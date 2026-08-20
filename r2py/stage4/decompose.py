"""Entity × effect-class score table (§7.4)."""
from __future__ import annotations

import re as _re
from typing import TYPE_CHECKING

from ..types import (
    ComparatorResult,
    EffectBundle,
    EffectClass,
    EntityId,
    EntityKind,
    EntityScore,
)

# Effect classes that feed into the side_effects sub-score.
_SIDE_EFFECT_CLASSES = frozenset({
    EffectClass.FILES,
    EffectClass.GRAPHICS,
    EffectClass.HTML,
    EffectClass.ENV,
    EffectClass.WARNINGS,
})


def _kind_scores(
    kind: EntityKind | None,
    data_score: float,
    stdout_score: float,
    executed_ok: bool,
    global_data_score: float,
) -> tuple[float, float, float]:
    """Return (type_match, control_flow_match, callable_output) for a given EntityKind.

    Uses comparator results already in hand as proxies — no per-entity sandbox needed:

    - LIBRARY_IMPORT: binary pass/fail on all three; callable_output N/A → 1.0.
    - VARIABLE / CONSTANT: data score captures type gate; sequential → executed_ok
      for control flow; not callable → 1.0.
    - FUNCTION_DEF: stdout is the best proxy for whether the function's control flow
      and output are correct across the script's calls; global data as callable proxy.
    - FUNCTION_CALL: call result (data_score) is type + control flow + callable output.
    - EXTERNAL_SYMBOL: treated like FUNCTION_DEF (external callable).
    - Others (FORMULA, S4_CLASS, R6_CLASS, ENVIRONMENT): executed_ok proxy; not callable.
    """
    ok = float(executed_ok)
    if kind == EntityKind.LIBRARY_IMPORT:
        return ok, ok, 1.0
    if kind in (EntityKind.VARIABLE, EntityKind.CONSTANT):
        return data_score, ok, 1.0
    if kind == EntityKind.FUNCTION_DEF:
        return ok, stdout_score, global_data_score
    if kind in (EntityKind.FUNCTION_CALL, EntityKind.EXTERNAL_SYMBOL):
        return data_score, data_score, data_score
    # FORMULA, S4_CLASS, R6_CLASS, ENVIRONMENT, or unknown
    return ok, ok, 1.0


def _parse_crash_line(stderr: str) -> int | None:
    """Extract the last crash line in _r2py_script.py from a Python traceback.

    Handles both bare filenames ('_r2py_script.py') and full temp paths
    ('.../tmpXXX/_r2py_script.py') as produced by Windows/Linux sandboxes.
    """
    matches = _re.findall(r'File ".*?_r2py_script\.py", line (\d+)', stderr)
    return int(matches[-1]) if matches else None


def _attribute_crash(
    crash_file_line: int,
    preamble_lines: int,
    entity_line_map: dict[str, tuple[int, int]],
) -> tuple[str | None, set[str]]:
    """Map a crash line (1-indexed in _r2py_script.py) to (crashing_eid, pre_crash_eids).

    pre_crash_eids: entities whose entire range precedes the crash line — they
    executed successfully and deserve partial credit (executed_ok=True).
    """
    source_crash_line = crash_file_line - preamble_lines  # 1-indexed in source
    crashing_eid: str | None = None
    pre_crash_eids: set[str] = set()
    for eid, (start, end) in entity_line_map.items():
        if start <= source_crash_line <= end:
            crashing_eid = eid
        elif end < source_crash_line:
            pre_crash_eids.add(eid)
    return crashing_eid, pre_crash_eids


def _compare_entity_bundles(
    r_eb: EffectBundle,
    py_eb: EffectBundle,
    data_compare: str = "auto",
    rtol: float = 1e-6,
    atol: float = 1e-9,
) -> dict[EffectClass, ComparatorResult]:
    """Run comparators on a pair of per-entity EffectBundle deltas.

    Only compares DATA, GRAPHICS, and STDOUT — the effect classes populated by
    the checkpoint mechanism.  Other classes are omitted so callers can detect
    absence via ``ec in results``.
    """
    from .comparators import COMPARATORS
    from .comparators.data import DataComparator as _DataComparator

    results: dict[EffectClass, ComparatorResult] = {}

    # DATA
    data_cmp = _DataComparator(data_compare=data_compare, rtol=rtol, atol=atol)
    results[EffectClass.DATA] = data_cmp.compare(
        r_eb.data, py_eb.data, uncapturable=py_eb.uncapturable
    )

    # STDOUT
    results[EffectClass.STDOUT] = COMPARATORS[EffectClass.STDOUT].compare(
        r_eb.stdout, py_eb.stdout
    )

    # GRAPHICS — prefer SSIM on real PNG snapshots when both sides have them;
    # otherwise fall back to count-only matching. (Per-entity bundles may carry
    # either: list[bytes] from the snapshot path, or an int count when the
    # snapshot failed or was absent.)
    r_graphics = r_eb.graphics or []
    py_graphics = py_eb.graphics or []

    def _has_real_bytes(g) -> bool:
        return isinstance(g, list) and any(isinstance(b, (bytes, bytearray)) and b for b in g)

    if _has_real_bytes(r_graphics) and _has_real_bytes(py_graphics):
        results[EffectClass.GRAPHICS] = COMPARATORS[EffectClass.GRAPHICS].compare(
            r_graphics, py_graphics
        )
    else:
        r_count = r_graphics if isinstance(r_graphics, int) else len(r_graphics)
        py_count = py_graphics if isinstance(py_graphics, int) else len(py_graphics)
        results[EffectClass.GRAPHICS] = COMPARATORS[EffectClass.GRAPHICS].compare(
            [b""] * r_count, [b""] * py_count
        )

    return results


def make_score_table(
    entities: dict,
    comparator_results: dict[EffectClass, ComparatorResult],
    py_exit_code: int = 0,
    entity_line_map: dict[str, tuple[int, int]] | None = None,
    py_stderr: str = "",
    preamble_lines: int = 0,
    r_entity_bundles: dict[str, EffectBundle] | None = None,
    py_entity_bundles: dict[str, EffectBundle] | None = None,
    data_compare: str = "auto",
    rtol: float = 1e-6,
    atol: float = 1e-9,
    verbose: bool = False,
) -> dict[EntityId, EntityScore]:
    """Map entities to EntityScores using comparator_results.

    When entity_line_map is provided (from Stage 2's stitch output), each entity
    is matched to its declared variable name and given a per-variable data score.
    Entities whose names are not in the DATA comparator's per_variable dict fall
    back to the whole-script aggregate.

    py_exit_code: exit code of the Python sandbox run.
    entity_line_map: optional EntityId → (start_line, end_line) from Stage 2.
    py_stderr: stderr from the Python sandbox (used for crash attribution).
    preamble_lines: lines before source in _r2py_script.py (from EffectBundle).
    """
    executed_ok = py_exit_code == 0
    data_result = comparator_results.get(EffectClass.DATA)
    if not executed_ok:
        # Python crashed: empty-vs-empty must not score as 1.0 (avoids inflated
        # scores when both R and Python produce no captured data).
        global_data_score = 0.0
        per_variable: dict[str, float] = {}
    else:
        global_data_score = data_result.score if data_result else 0.0
        per_variable = data_result.per_variable if data_result else {}

    stdout_result = comparator_results.get(EffectClass.STDOUT)
    stdout_score = stdout_result.score if stdout_result else float(executed_ok)

    # When HTML is present and scores well, FILES/ENV are likely rendering
    # artifacts (font downloads, internal options) — exclude from side_effects.
    html_result = comparator_results.get(EffectClass.HTML)
    html_dominant = (
        html_result is not None
        and html_result.score >= 0.7
        and (html_result.explanation or "").startswith("html_content_compared:")
    )
    _skip_if_html = frozenset({EffectClass.FILES, EffectClass.ENV})

    side_scores = [
        comparator_results[ec].score
        for ec in _SIDE_EFFECT_CLASSES
        if ec in comparator_results
        and not (html_dominant and ec in _skip_if_html)
    ]
    side_effects_score = sum(side_scores) / len(side_scores) if side_scores else 1.0

    # ── R bundle deduplication: effects should be scored exactly once ──────
    # When two entities share overlapping source spans (e.g. outer wrapper
    # contains inner library call), the R checkpoint ordering may attribute
    # effects to the outer entity that actually belong to the inner.  Clear
    # the outer entity's R bundle so it scores via empty-vs-empty instead.
    if r_entity_bundles:
        r_entity_bundles = dict(r_entity_bundles)  # don't mutate caller's dict
        _spans = {
            eid: getattr(entities.get(eid), "source_span", None)
            for eid in r_entity_bundles
        }
        for outer_eid, outer_sp in _spans.items():
            if outer_sp is None:
                continue
            outer_eb = r_entity_bundles.get(outer_eid)
            if outer_eb is None:
                continue
            # Check if any other entity is nested inside this one
            for inner_eid, inner_sp in _spans.items():
                if inner_eid == outer_eid or inner_sp is None:
                    continue
                # Inner is nested: starts at or after outer, ends at or before outer
                nested = (
                    (inner_sp.start_line > outer_sp.start_line
                     or (inner_sp.start_line == outer_sp.start_line
                         and inner_sp.start_col >= outer_sp.start_col))
                    and (inner_sp.end_line < outer_sp.end_line
                         or (inner_sp.end_line == outer_sp.end_line
                             and inner_sp.end_col <= outer_sp.end_col))
                )
                if not nested:
                    continue
                # Outer contains inner — outer's effects are owned by the inner.
                # Replace with an empty bundle so the outer scores via
                # empty-vs-empty (if Python is also silent for this entity).
                r_entity_bundles[outer_eid] = EffectBundle()
                break

    # Idea C: crash attribution — give partial credit to entities that ran before the crash.
    pre_crash_eids: set[str] = set()
    if not executed_ok and py_stderr and entity_line_map:
        crash_file_line = _parse_crash_line(py_stderr)
        if crash_file_line is not None:
            _, pre_crash_eids = _attribute_crash(crash_file_line, preamble_lines, entity_line_map)

    table: dict[EntityId, EntityScore] = {}
    for entity_id, entity in entities.items():
        entity_executed_ok = executed_ok or (entity_id in pre_crash_eids)

        # ── Per-entity bundle comparison (Option 2 scoring) ──────────────────
        r_eb = (r_entity_bundles or {}).get(entity_id)
        py_eb = (py_entity_bundles or {}).get(entity_id)

        # When the checkpointed R run executed (r_entity_bundles populated) but
        # this entity's checkpoint was never reached (e.g. placed inside an
        # unexecuted conditional branch), treat the R bundle as empty — the
        # entity produced no observable effects in R.
        if r_eb is None and r_entity_bundles:
            r_eb = EffectBundle()

        # Treat a missing py_eb as empty only when entity_line_map confirms Python
        # intentionally omitted this entity (map was provided but entity absent).
        # Without entity_line_map we can't tell omission from a failed checkpoint,
        # so fall through to the global-score fallback instead.
        if py_eb is None and entity_line_map is not None and entity_id not in entity_line_map:
            py_eb = EffectBundle()

        use_per_entity = r_eb is not None and py_eb is not None and entity_executed_ok
        if use_per_entity:
            eb_results = _compare_entity_bundles(
                r_eb, py_eb, data_compare=data_compare, rtol=rtol, atol=atol
            )

            # Build data_score from only the effects R actually produced.
            # An empty-vs-empty DATA comparison (= 1.0) must not mask a
            # graphics or stdout failure — only include an effect class in the
            # proxy when R genuinely emitted something for it.
            proxy_scores: list[float] = []
            if r_eb.data:
                proxy_scores.append(eb_results[EffectClass.DATA].score)
            r_graphics_count = (
                r_eb.graphics if isinstance(r_eb.graphics, int)
                else len(r_eb.graphics or [])
            )
            if r_graphics_count > 0:
                proxy_scores.append(
                    eb_results.get(EffectClass.GRAPHICS,
                                   ComparatorResult(effect_class=EffectClass.GRAPHICS,
                                                    score=0.0, verdict="fail")).score
                )
            if r_eb.stdout:
                proxy_scores.append(eb_results[EffectClass.STDOUT].score)

            if not proxy_scores:
                # R emitted nothing observable.  Check whether Python also
                # emitted nothing — if so, the entity is equivalent (both
                # sides are silent) and deserves 1.0 rather than falling
                # through to the potentially-unrelated global data score.
                py_graphics_count = (
                    py_eb.graphics if isinstance(py_eb.graphics, int)
                    else len(py_eb.graphics or [])
                )
                py_also_empty = (
                    not py_eb.data and not py_eb.stdout and py_graphics_count == 0
                )
                if py_also_empty:
                    if verbose:
                        print(
                            f"  [score] {entity_id}: empty-vs-empty -> 1.0 "
                            f"(both R and Python produced no observable effects)"
                        )
                    proxy_scores = [1.0]

            use_per_entity = bool(proxy_scores)

        if use_per_entity:
            data_score = sum(proxy_scores) / len(proxy_scores)

            # side_effects from per-entity GRAPHICS + STDOUT comparison
            entity_side_scores = [
                eb_results[ec].score
                for ec in _SIDE_EFFECT_CLASSES | {EffectClass.STDOUT}
                if ec in eb_results
            ]
            entity_side_effects = (
                sum(entity_side_scores) / len(entity_side_scores)
                if entity_side_scores else side_effects_score
            )
            entity_stdout_score = eb_results.get(EffectClass.STDOUT, ComparatorResult(
                effect_class=EffectClass.STDOUT, score=stdout_score, verdict="pass"
            )).score
        else:
            # ── Fallback: global scores ───────────────────────────────────────
            entity_name = getattr(entity, "name", None)
            if entity_name and entity_name in per_variable:
                data_score = per_variable[entity_name]
            else:
                data_score = global_data_score
            entity_side_effects = side_effects_score
            entity_stdout_score = stdout_score

        kind = getattr(entity, "kind", None)
        type_match, control_flow_match, callable_output = _kind_scores(
            kind, data_score, entity_stdout_score, entity_executed_ok, global_data_score,
        )

        table[entity_id] = EntityScore(
            entity_id=entity_id,
            executed_ok=entity_executed_ok,
            type_match=type_match,
            control_flow_match=control_flow_match,
            data_output=data_score,
            variable_output=data_score,
            callable_output=callable_output,
            side_effects=entity_side_effects,
        )
    return table

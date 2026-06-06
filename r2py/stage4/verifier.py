"""Stage 4 verifier orchestrator (§7.1, §7.4)."""
from __future__ import annotations

import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

from ..stage0.effects import bundle as _bundle_mod
from ..stage0.sandbox.py_sandbox import PySandbox
from ..types import (
    CaptureSpec,
    ComparatorResult,
    EffectBundle,
    EffectClass,
    EntityId,
    FeedbackItem,
    ScoreReport,
)
from .comparators import COMPARATORS
from .comparators.data import DataComparator as _DataComparator
from .decompose import make_score_table

if TYPE_CHECKING:
    from ..stage1.script_map import ScriptMap as _FullScriptMap


# All capturable effect classes for the Python sandbox run.
_ALL_CAPTURE: CaptureSpec = frozenset({
    EffectClass.STDOUT,
    EffectClass.FILES,
    EffectClass.GRAPHICS,
    EffectClass.DATA,
    EffectClass.HTML,
    EffectClass.ENV,
    EffectClass.WARNINGS,
    EffectClass.RNG,
})


def _get_r_bundle(script_map) -> EffectBundle:
    """Aggregate entity actual_bundles from the ScriptMap into one R ground-truth bundle.

    Deduplicates by object identity: all entities produced by Stage 1's main run
    share the same bundle object, so we merge each unique bundle exactly once.
    """
    seen_ids: set[int] = set()
    bundles: list[EffectBundle] = []
    for e in getattr(script_map, "entities", {}).values():
        ab = getattr(e, "actual_bundle", None)
        if ab is not None and id(ab) not in seen_ids:
            seen_ids.add(id(ab))
            bundles.append(ab)
    if bundles:
        return _bundle_mod.merge(bundles)
    # No entity bundles — return empty (all comparators will score as 1.0 empty-vs-empty)
    return EffectBundle()


def _compare_bundles(
    r_bundle: EffectBundle,
    py_bundle: EffectBundle,
    data_compare: str,
    rtol: float,
    atol: float,
) -> dict[EffectClass, ComparatorResult]:
    results: dict[EffectClass, ComparatorResult] = {}

    # STDOUT
    results[EffectClass.STDOUT] = COMPARATORS[EffectClass.STDOUT].compare(
        r_bundle.stdout, py_bundle.stdout
    )

    # WARNINGS
    results[EffectClass.WARNINGS] = COMPARATORS[EffectClass.WARNINGS].compare(
        r_bundle.warnings, py_bundle.warnings
    )

    # ENV
    results[EffectClass.ENV] = COMPARATORS[EffectClass.ENV].compare(
        r_bundle.env, py_bundle.env
    )

    # FILES
    results[EffectClass.FILES] = COMPARATORS[EffectClass.FILES].compare(
        r_bundle.files, py_bundle.files
    )

    # HTML
    results[EffectClass.HTML] = COMPARATORS[EffectClass.HTML].compare(
        r_bundle.html, py_bundle.html
    )

    # GRAPHICS
    results[EffectClass.GRAPHICS] = COMPARATORS[EffectClass.GRAPHICS].compare(
        r_bundle.graphics, py_bundle.graphics
    )

    # DATA — uses configurable data_compare + tolerance
    data_cmp = _DataComparator(data_compare=data_compare, rtol=rtol, atol=atol)
    results[EffectClass.DATA] = data_cmp.compare(
        r_bundle.data, py_bundle.data, uncapturable=py_bundle.uncapturable
    )

    return results


def _build_feedback(
    comparator_results: dict[EffectClass, ComparatorResult],
    entities: dict,
) -> list[FeedbackItem]:
    """Convert comparator results into FeedbackItems for Stage 3.

    Triggers on any partial score (score < 1.0), not just hard "fail", so
    pass_via_fallback results (e.g. score=0.603) generate actionable feedback
    instead of leaving Stage 3 with no signal.

    DATA failures: attributed to the specific entity whose name matches the
    failing variable, so Stage 3 targets the right entity. Non-DATA effects
    are broadcast to all entities (whole-script signal).
    """
    items: list[FeedbackItem] = []

    name_to_eid: dict[str, str] = {
        getattr(e, "name", None): eid
        for eid, e in entities.items()
        if getattr(e, "name", None)
    }

    for ec, result in comparator_results.items():
        if result.score >= 1.0:
            continue

        if ec == EffectClass.DATA and result.per_variable:
            for var_name, var_score in result.per_variable.items():
                if var_score >= 1.0:
                    continue
                expl = (
                    _extract_var_explanation(result.explanation, var_name)
                    or f"{var_name}: score {var_score:.3f}"
                )
                target_eid = name_to_eid.get(var_name)
                if target_eid:
                    items.append(FeedbackItem(
                        entity_id=target_eid,
                        effect_class=ec,
                        message=expl,
                        score=var_score,
                    ))
                else:
                    for eid in entities:
                        items.append(FeedbackItem(
                            entity_id=eid,
                            effect_class=ec,
                            message=expl,
                            score=var_score,
                        ))
        else:
            if not result.explanation:
                continue
            for entity_id in entities:
                items.append(FeedbackItem(
                    entity_id=entity_id,
                    effect_class=ec,
                    message=result.explanation,
                    score=result.score,
                ))

    return items


def _extract_var_explanation(full_explanation: str, var_name: str) -> str | None:
    """Extract the semicolon-delimited fragment for var_name from a joined explanation."""
    for fragment in full_explanation.split(";"):
        fragment = fragment.strip()
        if fragment.startswith(var_name + ":") or fragment.startswith(var_name + "["):
            return fragment
    return None


def get_r_bundle(script_map) -> EffectBundle:
    """Return the aggregated R ground-truth EffectBundle for *script_map*."""
    return _get_r_bundle(script_map)


# ---------------------------------------------------------------------------
# Per-entity Python checkpoint injection (Option 2 scoring)
# ---------------------------------------------------------------------------

# Preamble injected before the candidate Python script so _r2py_checkpoint is available.
_PY_CHECKPOINT_PREAMBLE = """\
import json as _r2py_json
import io as _r2py_io
import sys as _r2py_sys

_r2py_prev_ns: set = set()
_r2py_stdout_buf = _r2py_io.StringIO()
_r2py_real_stdout = _r2py_sys.stdout
_r2py_sys.stdout = type('_Tee', (), {
    'write': lambda s, x: (_r2py_stdout_buf.write(x), _r2py_real_stdout.write(x)),
    'flush': lambda s: (_r2py_stdout_buf.flush(), _r2py_real_stdout.flush()),
    'fileno': lambda s: _r2py_real_stdout.fileno(),
})()
_r2py_prev_stdout_pos = 0
_r2py_prev_fig_count = 0

def _r2py_checkpoint(eid):
    global _r2py_prev_ns, _r2py_prev_stdout_pos, _r2py_prev_fig_count
    try:
        import matplotlib.pyplot as _plt
        cur_fig_count = len(_plt.get_fignums())
    except Exception:
        cur_fig_count = 0
    graphics_delta = max(0, cur_fig_count - _r2py_prev_fig_count)

    cur_stdout = _r2py_stdout_buf.getvalue()
    stdout_delta = cur_stdout[_r2py_prev_stdout_pos:]

    g = globals()
    new_vars = {}
    uncapturable_vars = []
    for k, v in g.items():
        if k.startswith('_r2py') or k in _r2py_prev_ns:
            continue
        try:
            _r2py_serialized, _r2py_ok = _r2py_try_adapters(k, v)
            if not _r2py_ok:
                uncapturable_vars.append(k)
                continue
            _r2py_json.dumps(_r2py_serialized)
            new_vars[k] = _r2py_serialized
        except Exception:
            uncapturable_vars.append(k)

    safe_eid = eid.replace('/', '_').replace(':', '_')
    try:
        with open(f'_r2py_cp_{safe_eid}.json', 'w', encoding='utf-8') as _f:
            _r2py_json.dump({'data': new_vars, 'stdout': stdout_delta,
                             'graphics': graphics_delta,
                             'uncapturable': uncapturable_vars}, _f)
    except Exception:
        pass

    _r2py_prev_ns = set(k for k in g if not k.startswith('_r2py'))
    _r2py_prev_stdout_pos = len(cur_stdout)
    _r2py_prev_fig_count = cur_fig_count
"""


def _inject_py_checkpoints(
    py_source: str,
    entity_line_map: dict[str, tuple[int, int]],
) -> tuple[str, list[str]]:
    """Insert ``_r2py_checkpoint(eid)`` after each entity's last line.

    Inserts bottom-up so earlier line numbers are not disturbed.
    Returns ``(modified_source, ordered_eids)`` where ``ordered_eids`` lists
    the entity ids in ascending end-line order (for checkpoint file collection).
    """
    if not entity_line_map:
        return py_source, []

    lines = py_source.splitlines(keepends=True)
    # Sort by end_line ascending; process in reverse for bottom-up insertion.
    sorted_pairs = sorted(entity_line_map.items(), key=lambda kv: kv[1][1])
    ordered_eids = [eid for eid, _ in sorted_pairs]

    for eid, (_start, end_line) in reversed(sorted_pairs):
        # entity_line_map uses 1-based line numbers; convert to 0-based index.
        insert_idx = min(end_line, len(lines))  # insert after end_line (1-based → index)
        safe_eid = eid.replace("'", "\\'")
        checkpoint_line = f"_r2py_checkpoint('{safe_eid}')\n"
        lines.insert(insert_idx, checkpoint_line)

    return "".join(lines), ordered_eids


def _collect_py_checkpoints(
    workdir: "Path",
    eids: list[str],
) -> dict[str, EffectBundle]:
    """Read ``_r2py_cp_{eid}.json`` files from *workdir* and build EffectBundle deltas."""
    import json as _json

    result: dict[str, EffectBundle] = {}
    for eid in eids:
        safe_eid = eid.replace("/", "_").replace(":", "_")
        cp_path = workdir / f"_r2py_cp_{safe_eid}.json"
        if not cp_path.exists():
            continue
        try:
            cp = _json.loads(cp_path.read_text(encoding="utf-8"))
            raw_data = cp.get("data", {})
            # JSON null/array can appear when no new variables were captured; normalise.
            if not isinstance(raw_data, dict):
                raw_data = {}
            eb = EffectBundle(
                data=raw_data,
                stdout=cp.get("stdout", "") or "",
                graphics=cp.get("graphics", 0),  # type: ignore[arg-type]
            )
            eb.uncapturable.extend(cp.get("uncapturable", []))
            result[eid] = eb
        except Exception:
            continue
    return result


def verify(
    script_map,
    candidate: str,
    changed: list[str] | None = None,
    data_compare: str = "auto",
    rtol: float = 1e-6,
    atol: float = 1e-9,
    use_fuzz: bool = False,
    fuzz_n: int = 10,
    use_judge: bool = False,
    workdir: Path | None = None,
    timeout_s: float = 60,
    entity_line_map: dict | None = None,
    return_bundle: bool = False,
) -> "ScoreReport | tuple[ScoreReport, EffectBundle]":
    """Score a candidate Python translation against the R ScriptMap.

    changed: entity_ids touched by the last edit; if provided, only those
    entities are re-verified (incremental verification, §7.4).
    """
    entities = getattr(script_map, "entities", {})

    # --- Run candidate in Python sandbox ---
    r_bundle = _get_r_bundle(script_map)

    # Determine which effects were actually captured in R so we capture the same in Python
    capture = _ALL_CAPTURE

    # Inject per-entity checkpoint calls into the Python source (Option 2 scoring).
    py_source_checkpointed, cp_eids = _inject_py_checkpoints(candidate, entity_line_map or {})

    sandbox = PySandbox()
    if workdir is not None:
        py_bundle = sandbox.run(
            py_source_checkpointed, workdir=workdir, capture=capture,
            preamble=_PY_CHECKPOINT_PREAMBLE, timeout_s=timeout_s,
        )
        py_entity_bundles = _collect_py_checkpoints(workdir, cp_eids)
    else:
        with tempfile.TemporaryDirectory() as _tmpdir:
            _wd = Path(_tmpdir)
            py_bundle = sandbox.run(
                py_source_checkpointed, workdir=_wd, capture=capture,
                preamble=_PY_CHECKPOINT_PREAMBLE, timeout_s=timeout_s,
            )
            py_entity_bundles = _collect_py_checkpoints(_wd, cp_eids)

    # R per-entity bundles from Stage 1's checkpointed run.
    r_entity_bundles: dict[str, EffectBundle] = getattr(script_map, "entity_bundles", {})

    # --- Compare bundles ---
    comparator_results = _compare_bundles(r_bundle, py_bundle, data_compare, rtol, atol)

    # --- Score decomposition ---
    score_table = make_score_table(
        entities, comparator_results,
        py_exit_code=py_bundle.exit_code,
        entity_line_map=entity_line_map,
        py_stderr=py_bundle.stderr,
        preamble_lines=py_bundle.preamble_lines,
        r_entity_bundles=r_entity_bundles or None,
        py_entity_bundles=py_entity_bundles or None,
        data_compare=data_compare,
        rtol=rtol,
        atol=atol,
    )

    # --- Differential fuzzing (optional) ---
    feedback: list[FeedbackItem] = []
    if use_fuzz:
        from . import fuzz as _fuzz
        fuzz_cfg = _fuzz.FuzzConfig(n_inputs=fuzz_n)
        feedback.extend(_fuzz.run_fuzz(script_map, candidate, config=fuzz_cfg, data_compare=data_compare))

    feedback.extend(_build_feedback(comparator_results, entities))

    # Per-entity STDOUT feedback: detect R auto-print vs Python missing print.
    # When R produced stdout for an entity (auto-printed an unassigned expression)
    # but Python produced nothing, generate a targeted hint for that entity so
    # Stage 3 knows exactly what to fix rather than receiving only global noise.
    for eid, r_eb in (r_entity_bundles or {}).items():
        if not r_eb.stdout:
            continue
        py_eb = (py_entity_bundles or {}).get(eid)
        if py_eb is not None and not py_eb.stdout:
            feedback.append(FeedbackItem(
                entity_id=eid,
                effect_class=EffectClass.STDOUT,
                message=(
                    "R auto-prints this expression's result to stdout, "
                    "but Python produces no output for this entity. "
                    "Change the Python code or append to it so that it also prints to stdout."
                ),
                score=0.0,
            ))

    # RC2: surface crash traceback as feedback so Stage 3 knows what line failed.
    # Target the feedback to the entity that caused the crash (via crash attribution)
    # so _weak_first prioritises it. Fall back to all entities if unattributable.
    if py_bundle.exit_code != 0 and py_bundle.stderr:
        crash_msg = py_bundle.stderr.strip()
        if len(crash_msg) > 800:
            crash_msg = "..." + crash_msg[-800:]
        crash_target_ids: list[str] = []
        if entity_line_map:
            from .decompose import _parse_crash_line, _attribute_crash
            crash_line = _parse_crash_line(py_bundle.stderr)
            if crash_line is not None:
                crashing_eid, _ = _attribute_crash(
                    crash_line, py_bundle.preamble_lines, entity_line_map
                )
                if crashing_eid:
                    crash_target_ids = [crashing_eid]
        if not crash_target_ids:
            crash_target_ids = list(entities.keys())
        for entity_id in crash_target_ids:
            feedback.append(FeedbackItem(
                entity_id=entity_id,
                effect_class=EffectClass.SYNTAX,
                message=f"Python crashed (exit {py_bundle.exit_code}): {crash_msg}",
                score=0.0,
            ))

    # --- Uncomparable entities ---
    uncomparable: list[EntityId] = []
    data_result = comparator_results.get(EffectClass.DATA)
    if data_result and data_result.verdict == "uncomparable":
        uncomparable.extend(entities.keys())

    # --- Aggregate score ---
    # Per entity: average of all six EntityScore fields (kind-aware proxies populated by decompose).
    entity_scores = list(score_table.values())
    if entity_scores:
        per_entity_avgs = [
            (es.type_match + es.control_flow_match + es.data_output
             + es.variable_output + es.callable_output + es.side_effects) / 6
            for es in entity_scores
        ]
        aggregate = sum(per_entity_avgs) / len(per_entity_avgs)
    else:
        # No entities: score the raw effect comparison
        scored_results = [r for r in comparator_results.values() if r.verdict != "uncomparable"]
        aggregate = sum(r.score for r in scored_results) / len(scored_results) if scored_results else 1.0

    by_effect = {ec: result.score for ec, result in comparator_results.items()}

    report = ScoreReport(
        aggregate=aggregate,
        by_entity=score_table,
        by_effect=by_effect,
        uncomparable=uncomparable,
        feedback=feedback,
        py_exit_code=py_bundle.exit_code,
    )
    if return_bundle:
        return report, py_bundle
    return report

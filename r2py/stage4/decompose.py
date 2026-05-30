"""Entity × effect-class score table (§7.4)."""
from __future__ import annotations

import re as _re

from ..types import (
    ComparatorResult,
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
    """Extract the last crash line in _r2py_script.py from a Python traceback."""
    matches = _re.findall(r'File "_r2py_script\.py", line (\d+)', stderr)
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


def make_score_table(
    entities: dict,
    comparator_results: dict[EffectClass, ComparatorResult],
    py_exit_code: int = 0,
    entity_line_map: dict[str, tuple[int, int]] | None = None,
    py_stderr: str = "",
    preamble_lines: int = 0,
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

    side_scores = [
        comparator_results[ec].score
        for ec in _SIDE_EFFECT_CLASSES
        if ec in comparator_results
    ]
    side_effects_score = sum(side_scores) / len(side_scores) if side_scores else 1.0

    # Idea C: crash attribution — give partial credit to entities that ran before the crash.
    pre_crash_eids: set[str] = set()
    if not executed_ok and py_stderr and entity_line_map:
        crash_file_line = _parse_crash_line(py_stderr)
        if crash_file_line is not None:
            _, pre_crash_eids = _attribute_crash(crash_file_line, preamble_lines, entity_line_map)

    table: dict[EntityId, EntityScore] = {}
    for entity_id, entity in entities.items():
        entity_executed_ok = executed_ok or (entity_id in pre_crash_eids)

        entity_name = getattr(entity, "name", None)
        if entity_name and entity_name in per_variable:
            data_score = per_variable[entity_name]
        else:
            data_score = global_data_score

        kind = getattr(entity, "kind", None)
        type_match, control_flow_match, callable_output = _kind_scores(
            kind, data_score, stdout_score, entity_executed_ok, global_data_score,
        )

        table[entity_id] = EntityScore(
            entity_id=entity_id,
            executed_ok=entity_executed_ok,
            type_match=type_match,
            control_flow_match=control_flow_match,
            data_output=data_score,
            variable_output=data_score,
            callable_output=callable_output,
            side_effects=side_effects_score,
        )
    return table

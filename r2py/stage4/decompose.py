"""Entity × effect-class score table (§7.4)."""
from __future__ import annotations

from ..types import (
    ComparatorResult,
    EffectClass,
    EntityId,
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


def make_score_table(
    entities: dict,
    comparator_results: dict[EffectClass, ComparatorResult],
    py_exit_code: int = 0,
    entity_line_map: dict[str, tuple[int, int]] | None = None,
) -> dict[EntityId, EntityScore]:
    """Map entities to EntityScores using comparator_results.

    When entity_line_map is provided (from Stage 2's stitch output), each entity
    is matched to its declared variable name and given a per-variable data score.
    Entities whose names are not in the DATA comparator's per_variable dict fall
    back to the whole-script aggregate.

    py_exit_code: exit code of the Python sandbox run.
    entity_line_map: optional EntityId → (start_line, end_line) from Stage 2.
    """
    executed_ok = py_exit_code == 0
    data_result = comparator_results.get(EffectClass.DATA)
    global_data_score = data_result.score if data_result else 0.0
    per_variable = data_result.per_variable if data_result else {}

    side_scores = [
        comparator_results[ec].score
        for ec in _SIDE_EFFECT_CLASSES
        if ec in comparator_results
    ]
    side_effects_score = sum(side_scores) / len(side_scores) if side_scores else 1.0

    table: dict[EntityId, EntityScore] = {}
    for entity_id, entity in entities.items():
        # Try to assign a per-variable data score using the entity's name.
        entity_name = getattr(entity, "name", None)
        if entity_name and entity_name in per_variable:
            data_score = per_variable[entity_name]
        else:
            data_score = global_data_score

        table[entity_id] = EntityScore(
            entity_id=entity_id,
            executed_ok=executed_ok,
            # type_match / control_flow_match / callable_output: require per-entity
            # Python execution tracing; deferred (§7.4 note).
            type_match=0.0,
            control_flow_match=0.0,
            data_output=data_score,
            variable_output=data_score,
            callable_output=0.0,
            side_effects=side_effects_score,
        )
    return table

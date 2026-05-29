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
) -> dict[EntityId, EntityScore]:
    """Map entities to EntityScores using comparator_results.

    Each entity inherits the whole-script comparator results (since the Python
    candidate is run as a whole script, not per-entity). Per-entity slicing is
    deferred to the branch/replay path. For now, every entity gets the same
    effect-class scores, with variable_output / data_output populated from DATA.

    py_exit_code: exit code of the Python sandbox run.
    """
    executed_ok = py_exit_code == 0
    data_result = comparator_results.get(EffectClass.DATA)
    data_score = data_result.score if data_result else 0.0

    side_scores = [
        comparator_results[ec].score
        for ec in _SIDE_EFFECT_CLASSES
        if ec in comparator_results
    ]
    side_effects_score = sum(side_scores) / len(side_scores) if side_scores else 1.0

    table: dict[EntityId, EntityScore] = {}
    for entity_id in entities:
        table[entity_id] = EntityScore(
            entity_id=entity_id,
            executed_ok=executed_ok,
            # type_match / control_flow_match / callable_output: 0.0 until Stage 3
            # provides richer per-entity analysis (§7.4 note).
            type_match=0.0,
            control_flow_match=0.0,
            data_output=data_score,
            variable_output=data_score,
            callable_output=0.0,
            side_effects=side_effects_score,
        )
    return table

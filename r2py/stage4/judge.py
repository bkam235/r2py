"""Last-resort LLM judge — disabled by default (D4, §7.6)."""
from __future__ import annotations

from ..types import ComparatorResult, EffectClass


def judge_entity(
    entity,
    r_effect: object,
    py_effect: object,
    library=None,
    use_judge: bool = False,
) -> ComparatorResult | None:
    """Return a ComparatorResult from the LLM judge, or None if disabled.

    D4: use_judge=False by default. When disabled, returns None and the caller
    must treat the entity as uncomparable. Invoked only when all comparators
    return 'uncomparable' for an entity AND use_judge=True.

    Full LLM implementation is deferred to Stage 3 integration.
    """
    if not use_judge:
        return None

    # Stub — full implementation wired to the LLM in Stage 3 integration.
    return ComparatorResult(
        effect_class=EffectClass.DATA,
        score=0.0,
        verdict="uncomparable",
        explanation="LLM judge stub: not yet implemented.",
    )

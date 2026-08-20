"""Last-resort LLM judge — disabled by default (D4, §7.6)."""
from __future__ import annotations

import re as _re
import sys as _sys

from ..types import ComparatorResult, EffectClass

_SYSTEM = (
    "You are verifying whether two code snippets produce equivalent outputs. "
    "Reply with exactly <verdict>pass</verdict> or <verdict>fail</verdict> "
    "on its own line, followed by a one-sentence explanation. "
    "Only use the Pattern Library guidance provided — do not insist on exact "
    "R re-implementation."
)


def judge_entity(
    entity,
    r_effect: object,
    py_effect: object,
    library=None,
    use_judge: bool = False,
    model: str = "claude-sonnet-4-6",
) -> ComparatorResult | None:
    """Return a ComparatorResult from the LLM judge, or None if disabled.

    D4: use_judge=False by default. When disabled, returns None and the caller
    must treat the entity as uncomparable. Invoked only when all comparators
    return 'uncomparable' for an entity AND use_judge=True.
    """
    if not use_judge:
        return None

    from ..stage2 import llm as _llm

    # Gather Pattern Library guidance for context.
    guidance_lines: list[str] = []
    if library is not None and entity is not None:
        try:
            patterns = library.retrieve(entity, k=3)
            guidance_lines = [f"- {p.guidance}" for p in patterns if p.guidance]
        except Exception:
            pass
    guidance_text = "\n".join(guidance_lines) if guidance_lines else "(none)"

    msg = (
        f"R output:\n{r_effect}\n\n"
        f"Python output:\n{py_effect}\n\n"
        f"Pattern Library guidance:\n{guidance_text}"
    )

    try:
        raw = _llm.call(
            [{"role": "user", "content": msg}],
            system=_SYSTEM,
            model=model,
            max_tokens=256,
        )
    except Exception as exc:
        print(f"r2py: judge LLM call failed: {exc}", file=_sys.stderr)
        return ComparatorResult(
            effect_class=EffectClass.DATA,
            score=0.0,
            verdict="uncomparable",
            explanation=f"judge LLM error: {exc}",
        )

    raw_lower = raw.lower()
    if "<verdict>pass</verdict>" in raw_lower:
        verdict = "pass"
        score = 1.0
    elif "<verdict>fail</verdict>" in raw_lower:
        verdict = "fail"
        score = 0.0
    else:
        # LLM returned but included no verdict tag — treat as uncomparable.
        return ComparatorResult(
            effect_class=EffectClass.DATA,
            score=0.0,
            verdict="uncomparable",
            explanation=f"judge returned no verdict tag: {raw.strip()[:100]}",
        )

    # Strip verdict tags (case-insensitive) to get the explanation.
    explanation = _re.sub(
        r"<verdict>(?:pass|fail)</verdict>", "", raw, flags=_re.IGNORECASE
    ).strip()[:300]

    return ComparatorResult(
        effect_class=EffectClass.DATA,
        score=score,
        verdict=verdict,
        explanation=explanation,
    )

"""Stdout comparator (§7.3)."""
from __future__ import annotations

from ...types import ComparatorResult, EffectClass
from .base import text_similarity

_PASS_THRESHOLD = 0.95


class StdoutComparator:
    effect_class = EffectClass.STDOUT

    def compare(self, r_effect: str, py_effect: str) -> ComparatorResult:
        score = text_similarity(r_effect, py_effect)
        verdict = "pass" if score >= _PASS_THRESHOLD else "fail"
        explanation = "" if verdict == "pass" else f"stdout similarity {score:.3f} < {_PASS_THRESHOLD}"
        return ComparatorResult(
            effect_class=EffectClass.STDOUT,
            score=score,
            verdict=verdict,
            explanation=explanation,
        )

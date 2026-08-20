"""Warnings comparator (§7.3)."""
from __future__ import annotations

from ...types import ComparatorResult, EffectClass
from .base import text_similarity

_PASS_THRESHOLD = 0.95


class WarningsComparator:
    effect_class = EffectClass.WARNINGS

    def compare(self, r_effect: list[str], py_effect: list[str]) -> ComparatorResult:
        r_text = "\n".join(sorted(r_effect))
        py_text = "\n".join(sorted(py_effect))
        score = text_similarity(r_text, py_text)
        verdict = "pass" if score >= _PASS_THRESHOLD else "fail"
        explanation = "" if verdict == "pass" else f"warnings similarity {score:.3f} < {_PASS_THRESHOLD}"
        return ComparatorResult(
            effect_class=EffectClass.WARNINGS,
            score=score,
            verdict=verdict,
            explanation=explanation,
        )

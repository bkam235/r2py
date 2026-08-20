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
        if verdict == "pass":
            explanation = ""
        else:
            r_preview = repr(r_effect[:200]) if r_effect else "''"
            py_preview = repr(py_effect[:200]) if py_effect else "''"
            explanation = f"[STDOUT] score={score:.3f}: R printed {r_preview} but Python printed {py_preview}"
        return ComparatorResult(
            effect_class=EffectClass.STDOUT,
            score=score,
            verdict=verdict,
            explanation=explanation,
        )

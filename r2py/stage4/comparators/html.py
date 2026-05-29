"""HTML comparator — DOM-normalized text similarity (§7.3)."""
from __future__ import annotations

import re

from ...types import ComparatorResult, EffectClass
from .base import text_similarity

_PASS_THRESHOLD = 0.9
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def _normalize(html: str) -> str:
    text = _TAG_RE.sub(" ", html)
    return _WS_RE.sub(" ", text).strip()


class HtmlComparator:
    effect_class = EffectClass.HTML

    def compare(self, r_effect: list[str], py_effect: list[str]) -> ComparatorResult:
        if not r_effect and not py_effect:
            return ComparatorResult(effect_class=EffectClass.HTML, score=1.0, verdict="pass")

        if len(r_effect) != len(py_effect):
            return ComparatorResult(
                effect_class=EffectClass.HTML,
                score=0.0,
                verdict="fail",
                explanation=f"HTML item count differs: R={len(r_effect)} Python={len(py_effect)}",
                failure_tag="value",
            )

        scores = [
            text_similarity(_normalize(r), _normalize(p))
            for r, p in zip(r_effect, py_effect)
        ]
        score = sum(scores) / len(scores)
        verdict = "pass" if score >= _PASS_THRESHOLD else "fail"
        explanation = "" if verdict == "pass" else f"HTML similarity {score:.3f} < {_PASS_THRESHOLD}"
        return ComparatorResult(
            effect_class=EffectClass.HTML,
            score=score,
            verdict=verdict,
            explanation=explanation,
        )

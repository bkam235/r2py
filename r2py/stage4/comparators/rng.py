"""RNG sequence comparator (§7.3)."""
from __future__ import annotations

import math

from ...types import ComparatorResult, EffectClass

_RTOL = 1e-6
_ATOL = 1e-9


def _values_close(a: float, b: float) -> bool:
    try:
        return math.isclose(float(a), float(b), rel_tol=_RTOL, abs_tol=_ATOL)
    except (TypeError, ValueError):
        return str(a) == str(b)


class RngComparator:
    effect_class = EffectClass.RNG

    def compare(self, r_effect: list[tuple], py_effect: list[tuple]) -> ComparatorResult:
        if not r_effect and not py_effect:
            return ComparatorResult(effect_class=EffectClass.RNG, score=1.0, verdict="pass")

        if not r_effect or not py_effect:
            return ComparatorResult(
                effect_class=EffectClass.RNG,
                score=0.0,
                verdict="fail",
                explanation=(
                    f"RNG sequence length mismatch: R={len(r_effect)} Python={len(py_effect)}"
                ),
                failure_tag="value",
            )

        r_vals = [entry[-1] if isinstance(entry, (list, tuple)) else entry for entry in r_effect]
        py_vals = [entry[-1] if isinstance(entry, (list, tuple)) else entry for entry in py_effect]

        if len(r_vals) != len(py_vals):
            score = min(len(r_vals), len(py_vals)) / max(len(r_vals), len(py_vals))
            return ComparatorResult(
                effect_class=EffectClass.RNG,
                score=score,
                verdict="fail",
                explanation=f"RNG call count differs: R={len(r_vals)} Python={len(py_vals)}",
                failure_tag="value",
            )

        matching = sum(1 for r, p in zip(r_vals, py_vals) if _values_close(r, p))
        score = matching / len(r_vals)
        verdict = "pass" if score >= 1.0 else "fail"
        explanation = "" if verdict == "pass" else (
            f"RNG values match {matching}/{len(r_vals)}"
        )

        return ComparatorResult(
            effect_class=EffectClass.RNG,
            score=score,
            verdict=verdict,
            explanation=explanation,
            failure_tag="value" if verdict == "fail" else None,
        )

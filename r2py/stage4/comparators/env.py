"""Environment comparator — exact JSON diff (§7.3)."""
from __future__ import annotations

from ...types import ComparatorResult, EffectClass


class EnvComparator:
    effect_class = EffectClass.ENV

    def compare(self, r_effect: dict, py_effect: dict) -> ComparatorResult:
        if r_effect == py_effect:
            return ComparatorResult(
                effect_class=EffectClass.ENV,
                score=1.0,
                verdict="pass",
            )

        only_r = sorted(set(r_effect) - set(py_effect))
        only_py = sorted(set(py_effect) - set(r_effect))
        differing = sorted(
            k for k in set(r_effect) & set(py_effect) if r_effect[k] != py_effect[k]
        )
        parts: list[str] = []
        if only_r:
            parts.append(f"only in R: {only_r}")
        if only_py:
            parts.append(f"only in Python: {only_py}")
        if differing:
            parts.append(f"differing values: {differing}")

        return ComparatorResult(
            effect_class=EffectClass.ENV,
            score=0.0,
            verdict="fail",
            explanation="; ".join(parts),
            failure_tag="value",
        )

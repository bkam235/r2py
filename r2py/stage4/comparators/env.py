"""Environment comparator — exact JSON diff of what R changed (§7.3)."""
from __future__ import annotations

from ...types import ComparatorResult, EffectClass


def _comparable(effect: dict) -> dict:
    """Drop R ``options()`` diffs: packages set them on load (e.g. cli's callr option) and
    Python has no equivalent, so they made every correct translation score 0 (Stage 0b)."""
    return {k: v for k, v in effect.items() if not k.startswith("option:")}


class EnvComparator:
    effect_class = EffectClass.ENV

    def compare(self, r_effect: dict, py_effect: dict) -> ComparatorResult:
        r_effect, py_effect = _comparable(r_effect), _comparable(py_effect)
        # Only what R changed must be reproduced.  Python-only changes are library side effects
        # (importing numpy/sklearn sets KMP_DUPLICATE_LIB_OK, KMP_INIT_AT_FORK; sys_path grows)
        # that R can never show, so they must not fail a correct translation.
        py_effect = {k: v for k, v in py_effect.items() if k in r_effect}
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

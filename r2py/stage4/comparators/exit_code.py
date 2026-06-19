"""Exit code symmetry comparator — scores whether R and Python agree on crash vs. success."""
from __future__ import annotations

from ...types import ComparatorResult, EffectClass


class ExitCodeComparator:
    effect_class = EffectClass.SYNTAX

    def compare(self, r_exit_code: int, py_exit_code: int) -> ComparatorResult:
        if r_exit_code == 0 and py_exit_code == 0:
            return ComparatorResult(
                effect_class=EffectClass.SYNTAX, score=1.0, verdict="pass",
            )
        if r_exit_code != 0 and py_exit_code != 0:
            return ComparatorResult(
                effect_class=EffectClass.SYNTAX, score=0.8, verdict="pass",
                explanation="Both R and Python exit non-zero (error symmetry).",
            )
        if r_exit_code == 0:
            return ComparatorResult(
                effect_class=EffectClass.SYNTAX, score=0.0, verdict="fail",
                explanation=f"R succeeded but Python crashed (exit {py_exit_code}).",
            )
        return ComparatorResult(
            effect_class=EffectClass.SYNTAX, score=0.0, verdict="fail",
            explanation=f"R errored (exit {r_exit_code}) but Python succeeded — missing error handling.",
        )

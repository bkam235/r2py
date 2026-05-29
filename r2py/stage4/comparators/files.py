"""Files comparator — sha256 hash comparison (§7.3)."""
from __future__ import annotations

from ...types import ComparatorResult, EffectClass


class FilesComparator:
    effect_class = EffectClass.FILES

    def compare(self, r_effect: dict[str, str], py_effect: dict[str, str]) -> ComparatorResult:
        """Compare dicts of path → sha256 hex.

        Score = fraction of R-written paths where the sha256 matches in Python.
        Files only in Python are ignored. Files only in R reduce the score.
        """
        if not r_effect and not py_effect:
            return ComparatorResult(effect_class=EffectClass.FILES, score=1.0, verdict="pass")

        if not r_effect:
            return ComparatorResult(
                effect_class=EffectClass.FILES,
                score=0.0,
                verdict="fail",
                explanation="R wrote no files but Python wrote some",
                failure_tag="value",
            )

        matching = sum(1 for path, sha in r_effect.items() if py_effect.get(path) == sha)
        score = matching / len(r_effect)
        verdict = "pass" if score == 1.0 else "fail"

        explanation = ""
        if verdict == "fail":
            missing = [p for p in r_effect if p not in py_effect]
            wrong = [p for p in r_effect if p in py_effect and py_effect[p] != r_effect[p]]
            parts = []
            if missing:
                parts.append(f"missing: {missing}")
            if wrong:
                parts.append(f"hash mismatch: {wrong}")
            explanation = "; ".join(parts)

        return ComparatorResult(
            effect_class=EffectClass.FILES,
            score=score,
            verdict=verdict,
            explanation=explanation,
            failure_tag="value" if verdict == "fail" else None,
        )

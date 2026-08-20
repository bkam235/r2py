"""Files comparator — sha256 hash comparison with text content fallback (§7.3)."""
from __future__ import annotations

from ...types import ComparatorResult, EffectClass
from .base import text_similarity

_TEXT_EXTENSIONS = frozenset({".csv", ".txt", ".json", ".tsv", ".xml", ".yaml", ".yml", ".log"})


def _is_text_file(path: str) -> bool:
    return any(path.lower().endswith(ext) for ext in _TEXT_EXTENSIONS)


class FilesComparator:
    effect_class = EffectClass.FILES

    def __init__(self, r_file_contents: dict[str, str] | None = None,
                 py_file_contents: dict[str, str] | None = None):
        self._r_contents = r_file_contents or {}
        self._py_contents = py_file_contents or {}

    def compare(self, r_effect: dict[str, str], py_effect: dict[str, str]) -> ComparatorResult:
        """Compare dicts of path -> sha256 hex.

        Score = fraction of R-written paths where the sha256 matches in Python.
        For text files with hash mismatches, falls back to content similarity
        to tolerate formatting differences (line endings, trailing newlines).
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

        scores: list[float] = []
        for path, sha in r_effect.items():
            if py_effect.get(path) == sha:
                scores.append(1.0)
            elif path in py_effect and _is_text_file(path):
                r_text = self._r_contents.get(path, "")
                py_text = self._py_contents.get(path, "")
                if r_text and py_text:
                    scores.append(text_similarity(r_text.strip(), py_text.strip()))
                else:
                    scores.append(0.0)
            elif path in py_effect:
                scores.append(0.0)
            else:
                scores.append(0.0)

        score = sum(scores) / len(scores) if scores else 0.0
        verdict = "pass" if score >= 1.0 else "fail"

        explanation = ""
        if verdict == "fail":
            missing = [p for p in r_effect if p not in py_effect]
            wrong = [p for p in r_effect if p in py_effect and py_effect[p] != r_effect[p]]
            parts = []
            if missing:
                parts.append(f"missing: {missing}")
            if wrong:
                parts.append(f"content differs: {wrong}")
            explanation = "; ".join(parts)

        return ComparatorResult(
            effect_class=EffectClass.FILES,
            score=score,
            verdict=verdict,
            explanation=explanation,
            failure_tag="value" if verdict == "fail" else None,
        )

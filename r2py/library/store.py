"""Filesystem store for Pattern Library (§6.1)."""
from __future__ import annotations

from pathlib import Path

from .pattern import Pattern, from_markdown, to_markdown
from ..types import PatternId


class PatternStore:
    """Manages one .md file per pattern under library_dir/patterns/."""

    def __init__(self, library_dir: Path) -> None:
        self._dir = library_dir / "patterns"
        self._dir.mkdir(parents=True, exist_ok=True)

    def _path(self, pattern_id: PatternId) -> Path:
        """Canonical save path: always a flat file directly under patterns/."""
        return self._dir / f"{pattern_id}.md"

    def save(self, pattern: Pattern) -> None:
        self._path(pattern.id).write_text(to_markdown(pattern), encoding="utf-8")

    def get(self, pattern_id: PatternId) -> Pattern | None:
        # Try the canonical flat path first (fast).
        p = self._path(pattern_id)
        if p.exists():
            return from_markdown(p.read_text(encoding="utf-8"))
        # Fall back to recursive search so files in subdirectories (e.g. seed
        # collections) are still findable — matches the rglob in load_all().
        matches = list(self._dir.rglob(f"{pattern_id}.md"))
        if not matches:
            return None
        return from_markdown(matches[0].read_text(encoding="utf-8"))

    def load_all(self) -> dict[PatternId, Pattern]:
        result: dict[PatternId, Pattern] = {}
        for md_file in self._dir.rglob("*.md"):
            try:
                pat = from_markdown(md_file.read_text(encoding="utf-8"))
                result[pat.id] = pat
            except (ValueError, KeyError):
                pass
        return result

    def list_ids(self) -> list[PatternId]:
        return [p.stem for p in self._dir.rglob("*.md")]

    def delete(self, pattern_id: PatternId) -> None:
        p = self._path(pattern_id)
        if p.exists():
            p.unlink()

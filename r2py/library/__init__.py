"""Pattern Library — the verified skill wiki (§6).

Read by Stage 2 (retrieval), written only by Stage 4 (wiki_update.py).
"""
from __future__ import annotations

from pathlib import Path

from ..types import Edit, PatternId
from .pattern import Pattern
from .store import PatternStore
from .index import PatternIndex
from . import retrieval as _retrieval
from . import writer as _writer


class PatternLibrary:
    """Facade wiring PatternStore + PatternIndex + writer module."""

    def __init__(self, library_dir: Path) -> None:
        self._dir = library_dir
        self.store = PatternStore(library_dir)
        self.index = PatternIndex(library_dir)
        # Build index on first use if it is empty
        if not self.index.all_ids():
            self.index.rebuild(self.store)

    # ------------------------------------------------------------------ #
    # Read path (Stage 2)                                                  #
    # ------------------------------------------------------------------ #

    def retrieve(
        self,
        entity: object,
        k: int = 3,
        no_seeds: bool = False,
    ) -> list[Pattern]:
        return _retrieval.retrieve(entity, k, self.store, self.index, no_seeds=no_seeds)

    # ------------------------------------------------------------------ #
    # Write path (Stage 4 / loop — routed through writer)                 #
    # ------------------------------------------------------------------ #

    def record_evidence(
        self,
        edit: Edit,
        score_delta: float,
        script_id: str = "",
        entity_id: str = "",
        verification_path: str = "exact",
    ) -> None:
        _writer.record_evidence(
            edit, score_delta, script_id, entity_id, verification_path,
            self.store, self.index,
        )

    def record_tie(
        self,
        edit: Edit,
        script_id: str = "",
        entity_id: str = "",
    ) -> None:
        _writer.record_tie(edit, script_id, entity_id, self.store, self.index)

    def record_contradiction(
        self,
        edit: Edit,
        observed: float,
        script_id: str = "",
        entity_id: str = "",
    ) -> None:
        _writer.record_contradiction(
            edit, observed, script_id, entity_id, self.store, self.index,
        )

    def __repr__(self) -> str:
        n = len(self.index.all_ids())
        return f"PatternLibrary(dir={self._dir}, patterns={n})"


def get_library(library_dir: Path | str | None = None) -> PatternLibrary:
    """Return a PatternLibrary rooted at library_dir (default: work/library/)."""
    if library_dir is None:
        library_dir = Path("work") / "library"
    return PatternLibrary(Path(library_dir))

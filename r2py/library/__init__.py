"""Pattern Library — the verified skill wiki (§6).

Read by Stage 2 (retrieval), written only by Stage 4 (wiki_update.py).
"""
from __future__ import annotations

from pathlib import Path

from ..types import Edit
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
        # D6 optional learned retrieval reranker — currently a no-op.
        self._learned_retrieval: bool = False
        self._reranker_model: object = None
        self._models_loaded: bool = False

    @property
    def learned_retrieval(self) -> bool:
        return self._learned_retrieval

    @learned_retrieval.setter
    def learned_retrieval(self, value: bool) -> None:
        if value != self._learned_retrieval:
            self._models_loaded = False
        self._learned_retrieval = value

    def _ensure_models_loaded(self) -> None:
        if self._models_loaded:
            return
        self._models_loaded = True
        if self._learned_retrieval:
            _models_dir = self._dir.parent / "models"
            from . import reranker as _reranker
            self._reranker_model = _reranker.load_model(_models_dir / "reranker")

    # ------------------------------------------------------------------ #
    # Read path (Stage 2)                                                  #
    # ------------------------------------------------------------------ #

    def retrieve(
        self,
        entity: object,
        k: int = 3,
        no_seeds: bool = False,
    ) -> list[Pattern]:
        candidates = _retrieval.retrieve(entity, k, self.store, self.index,
                                         no_seeds=no_seeds)
        if self.learned_retrieval:
            self._ensure_models_loaded()
            if self._reranker_model is not None:
                from . import reranker as _reranker
                candidates = _reranker.rerank(entity, candidates, self._reranker_model)
        return candidates

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
        ast_shape_hash: str = "",
        entity_package: str = "",
        r_snippet: str = "",
        py_snippet: str = "",
        failure_class: str = "",
        old_code: str = "",
        new_code: str = "",
    ) -> None:
        _writer.record_evidence(
            edit, score_delta, script_id, entity_id, verification_path,
            self.store, self.index, ast_shape_hash, entity_package,
            r_snippet=r_snippet, py_snippet=py_snippet,
            failure_class=failure_class, old_code=old_code, new_code=new_code,
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

    def epistemology_review(self) -> list[str]:
        from . import epistemology as _epi
        return _epi.review(self.store, self.index)

    def __repr__(self) -> str:
        n = len(self.index.all_ids())
        return f"PatternLibrary(dir={self._dir}, patterns={n})"


def get_library(library_dir: Path | str | None = None) -> PatternLibrary:
    """Return a PatternLibrary rooted at library_dir (default: work/library/)."""
    if library_dir is None:
        library_dir = Path("work") / "library"
    return PatternLibrary(Path(library_dir))

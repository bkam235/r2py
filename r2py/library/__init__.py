"""Pattern Library — the verified skill wiki (§6).

Read by Stage 2 (retrieval), written only by Stage 4 (wiki_update.py).
"""
from __future__ import annotations

from ..types import Edit


class _StubLibrary:
    """Placeholder satisfying the LibraryProtocol used by the loop."""

    def record_evidence(self, edit: Edit, score_delta: float) -> None:
        raise NotImplementedError("Pattern Library not yet implemented")

    def record_tie(self, edit: Edit) -> None:
        raise NotImplementedError("Pattern Library not yet implemented")

    def record_contradiction(self, edit: Edit, observed: float) -> None:
        raise NotImplementedError("Pattern Library not yet implemented")


def get_library() -> _StubLibrary:
    """Return the active Pattern Library instance."""
    raise NotImplementedError("Pattern Library not yet implemented (architecture step 3)")

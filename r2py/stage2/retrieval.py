"""Pattern Library retrieval for Stage 2 (§5.3, §6.4)."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..stage1.entities import Entity
    from ..library import PatternLibrary
    from ..library.pattern import Pattern


def retrieve_patterns(
    entity: "Entity",
    library: "PatternLibrary",
    no_seeds: bool = False,
) -> list["Pattern"]:
    """Return up to 3 patterns relevant to entity, ranked per §6.4."""
    return library.retrieve(entity, k=3, no_seeds=no_seeds)

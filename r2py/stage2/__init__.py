"""Stage 2 — Translation: entity-by-entity LLM translation (§5)."""
from __future__ import annotations

from .translator import translate as _translate

from ..types import ScriptMap


def translate(
    script_map: ScriptMap,
    library: object | None = None,
    **kwargs,
) -> tuple[str, dict]:
    """Produce a (python_source, entity_line_map) tuple from a ScriptMap.

    entity_line_map maps EntityId → (start_line, end_line) (1-indexed, inclusive)
    for each entity's body block in the assembled Python source.  The map may be
    empty when the coherence pass rewrites the source (line numbers shift).

    Args:
        script_map: Stage 1 ScriptMap.
        library: PatternLibrary (defaults to work/library/ on disk).
    """
    if library is None:
        from ..library import get_library
        library = get_library()
    return _translate(script_map, library, **kwargs)

"""Stage 2 — Translation: entity-by-entity LLM translation (§5)."""
from __future__ import annotations

from .translator import translate as _translate

from ..types import ScriptMap


def translate(script_map: ScriptMap, library: object | None = None) -> str:
    """Produce a Python source string from a ScriptMap.

    Args:
        script_map: Stage 1 ScriptMap.
        library: PatternLibrary (defaults to work/library/ on disk).
    """
    if library is None:
        from ..library import get_library
        library = get_library()
    return _translate(script_map, library)

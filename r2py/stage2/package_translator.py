"""Translate ExternalSymbol R sources for Stage 2 (§5.4)."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from .prompt import SYSTEM_PROMPT, build_entity_prompt, parse_entity_response
from . import llm as _llm

if TYPE_CHECKING:
    from ..stage1.entities import Entity
    from ..stage1.script_map import ScriptMap
    from ..library import PatternLibrary

# Recursion guard: packages currently being translated in ancestor frames.
_in_progress: set[str] = set()

_DEFAULT_CACHE_DIR = Path("work") / "translated_packages"


def translate_external_symbol(
    entity: "Entity",
    script_map: "ScriptMap",
    library: "PatternLibrary",
    cache_dir: Path = _DEFAULT_CACHE_DIR,
    model: str = _llm._DEFAULT_MODEL,
) -> str | None:
    """Return a Python snippet for an ExternalSymbol entity, using a cache.

    Returns None if:
    - The entity has no source location in script_map.external_sources.
    - The entity's package is currently being translated (recursion guard).
    - The LLM call fails.
    """
    pkg = entity.package or ""
    if not pkg:
        return None

    # Recursion guard
    if pkg in _in_progress:
        return None

    # Source location required
    source_loc = script_map.external_sources.get(entity.id)
    if source_loc is None:
        return None

    # Cache lookup
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_key = f"{pkg}__{entity.name}.py"
    cache_path = cache_dir / cache_key
    if cache_path.exists():
        return cache_path.read_text(encoding="utf-8")

    # Read R source for this symbol
    r_source = _read_r_source(source_loc)
    if not r_source:
        return None

    _in_progress.add(pkg)
    try:
        messages = build_entity_prompt(entity, script_map, [], {})
        # Prepend the actual R source from the package file
        if messages:
            messages[0]["content"] = (
                f"## Package source for {pkg}::{entity.name}\n```r\n{r_source}\n```\n\n"
                + messages[0]["content"]
            )
        raw = _llm.call(messages, SYSTEM_PROMPT, model=model)
        snippet, _imports, _effects = parse_entity_response(raw)
        cache_path.write_text(snippet, encoding="utf-8")
        return snippet
    except Exception:
        return None
    finally:
        _in_progress.discard(pkg)


def _read_r_source(source_loc: object) -> str:
    """Read the R source text for a SourceLocation, returning empty string on failure."""
    try:
        from ..stage1.entities import SourceLocation
        if not isinstance(source_loc, SourceLocation):
            return ""
        path = Path(source_loc.file)
        if not path.exists():
            return ""
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        start = max(0, source_loc.start_line - 1)
        end = min(len(lines), source_loc.end_line)
        return "\n".join(lines[start:end])
    except Exception:
        return ""

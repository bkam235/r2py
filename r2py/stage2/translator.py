"""Stage 2 translation orchestrator (§5.3–§5.6)."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from . import llm as _llm
from . import walker as _walker
from . import retrieval as _retrieval
from . import package_translator as _pkg_trans
from . import stitch as _stitch
from . import coherence as _coherence
from .prompt import SYSTEM_PROMPT, build_entity_prompt, parse_entity_response

if TYPE_CHECKING:
    from ..stage1.script_map import ScriptMap
    from ..library import PatternLibrary

from ..types import EntityKind


def translate(
    script_map: "ScriptMap",
    library: "PatternLibrary",
    *,
    no_seeds: bool = False,
    model: str = _llm._DEFAULT_MODEL,
    cache_dir: Path | None = None,
    run_coherence: bool = True,
    r_path: str = "",
) -> tuple[str, dict[str, tuple[int, int]]]:
    """Translate a ScriptMap to a Python source string.

    Procedure (§5.3–§5.6):
    1. Walk entities in topological (dependency-first) order.
    2. For each entity, retrieve patterns, build prompt, call LLM, parse output.
    3. Stitch per-entity snippets into one .py file.
    4. Run the whole-program coherence pass (§5.6).
    """
    if cache_dir is None:
        cache_dir = Path("work") / "translated_packages"

    entities = script_map.entities if hasattr(script_map, "entities") else {}
    order = _walker.topological_order(entities)

    per_entity: dict[str, str] = {}
    per_entity_imports: dict[str, list[str]] = {}
    per_entity_effects: dict[str, list[str]] = {}
    prior_translations: dict[str, str] = {}

    for eid in order:
        entity = entities[eid]

        # Retrieve patterns from the library
        patterns = _retrieval.retrieve_patterns(entity, library, no_seeds=no_seeds)

        # For ExternalSymbol entities, attempt a cached package translation
        ext_snippet: str | None = None
        if entity.kind == EntityKind.EXTERNAL_SYMBOL:
            ext_snippet = _pkg_trans.translate_external_symbol(
                entity, script_map, library, cache_dir=cache_dir, model=model
            )

        if ext_snippet is not None:
            # Use the cached/translated package snippet directly
            per_entity[eid] = ext_snippet
            per_entity_imports[eid] = []
            prior_translations[eid] = ext_snippet
            continue

        # General entity: build prompt and call LLM
        messages = build_entity_prompt(entity, script_map, patterns, prior_translations)
        try:
            raw = _llm.call(messages, SYSTEM_PROMPT, model=model)
            snippet, imports, effects = parse_entity_response(raw)
        except Exception as exc:
            print(f"r2py: LLM call failed for entity {eid}: {exc}", file=sys.stderr)
            snippet = f"# r2py: translation failed for {eid}"
            imports = []
            effects = []

        per_entity[eid] = snippet
        per_entity_imports[eid] = imports
        per_entity_effects[eid] = effects
        prior_translations[eid] = snippet

    # Make declared effects available to downstream stages (e.g. Stage 4 verify).
    try:
        script_map._stage2_declared_effects = per_entity_effects  # type: ignore[attr-defined]
    except AttributeError:
        pass  # frozen dataclass — callers can read per_entity_effects from the return value if needed

    python_source, entity_line_map = _stitch.compose(
        per_entity, per_entity_imports, order, script_map, model, r_path=r_path
    )

    if run_coherence:
        # Coherence edits may shift line numbers; invalidate the map to avoid
        # stale mappings.  TODO: rebuild entity_line_map from the revised source.
        revised, _edits = _coherence.review(
            python_source, script_map, library, model=model
        )
        if revised != python_source:
            python_source = revised
            entity_line_map = {}   # invalidated by coherence edits

    return python_source, entity_line_map

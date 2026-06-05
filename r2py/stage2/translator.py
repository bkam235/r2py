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
    prior_failures: dict[str, list[str]] | None = None,
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
    already_defined_names: set[str] = set()  # helper names defined by all prior entities

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
            already_defined_names.update(_stitch.get_toplevel_def_names(ext_snippet))
            continue

        # For VARIABLE entities with a simple (non-dict) R-captured value, generate
        # the assignment directly rather than going through the LLM. This avoids
        # cases where the LLM miscopies non-ASCII characters (e.g. é→è).
        cap_snippet = _generate_from_capture(entity)
        if cap_snippet is not None:
            per_entity[eid] = cap_snippet
            per_entity_imports[eid] = []
            per_entity_effects[eid] = []
            prior_translations[eid] = cap_snippet
            already_defined_names.update(_stitch.get_toplevel_def_names(cap_snippet))
            continue

        # General entity: build prompt and call LLM
        entity_failures = (prior_failures or {}).get(eid)
        messages = build_entity_prompt(
            entity, script_map, patterns, prior_translations, entity_failures,
            already_defined=already_defined_names,
        )
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
        already_defined_names.update(_stitch.get_toplevel_def_names(snippet))

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
            entity_line_map = _stitch.rebuild_entity_line_map(python_source)

    return python_source, entity_line_map


def retranslate_entity(
    eid: str,
    script_map: "ScriptMap",
    library: "PatternLibrary",
    *,
    model: str = _llm._DEFAULT_MODEL,
    cache_dir: Path | None = None,
    current_source: str = "",
) -> str | None:
    """Re-translate a single entity via stage 2, returning its new snippet.

    Used by stage 3's RETRANSLATE_ENTITY edit kind to recover entities whose
    initial translation produced a stub.  Extracts prior translations and
    already-defined names from *current_source* so the LLM has full context.

    Returns the new Python snippet, or None if the LLM call fails or produces
    another stub.
    """
    if cache_dir is None:
        cache_dir = Path("work") / "translated_packages"

    entities = script_map.entities if hasattr(script_map, "entities") else {}
    entity = entities.get(eid)
    if entity is None:
        return None

    prior_translations = _prior_translations_from_source(current_source, eid)
    already_defined = _already_defined_before(current_source, eid)

    patterns = _retrieval.retrieve_patterns(entity, library, no_seeds=False)
    messages = build_entity_prompt(
        entity, script_map, patterns, prior_translations,
        already_defined=already_defined,
    )
    try:
        raw = _llm.call(messages, SYSTEM_PROMPT, model=model)
        snippet, _imports, _effects = parse_entity_response(raw)
    except Exception as exc:
        print(f"r2py: retranslate_entity failed for {eid}: {exc}", file=sys.stderr)
        return None

    _STUB = "pass  # r2py: translation failed for entity (LLM response not valid Python)"
    if snippet.strip() == _STUB:
        return None
    return snippet


def _prior_translations_from_source(source: str, exclude_eid: str) -> dict[str, str]:
    """Extract per-entity body snippets from an assembled translation string.

    Keyed by entity_id; the target entity is excluded so it is not shown as its
    own dependency.
    """
    from .stitch import _SENTINEL_RE
    lines = source.splitlines()
    result: dict[str, str] = {}
    current_eid: str | None = None
    current_lines: list[str] = []
    for line in lines:
        m = _SENTINEL_RE.match(line)
        if m:
            if current_eid is not None and current_eid != exclude_eid:
                result[current_eid] = "\n".join(current_lines).strip()
            current_eid = m.group(1)
            current_lines = []
        elif current_eid is not None:
            current_lines.append(line)
    if current_eid is not None and current_eid != exclude_eid:
        result[current_eid] = "\n".join(current_lines).strip()
    return result


def _already_defined_before(source: str, target_eid: str) -> set[str]:
    """Return top-level def/class names and _-prefixed constants from before *target_eid*'s sentinel."""
    from .stitch import _SENTINEL_RE, get_toplevel_def_names
    lines = source.splitlines()
    before_lines: list[str] = []
    for line in lines:
        m = _SENTINEL_RE.match(line)
        if m and m.group(1) == target_eid:
            break
        before_lines.append(line)
    return get_toplevel_def_names("\n".join(before_lines))


def _generate_from_capture(entity) -> str | None:
    """Return a Python assignment snippet for a VARIABLE entity from its R-captured value.

    Only generates for simple non-dict values (lists of scalars, plain scalars).
    Returns None if the entity is not VARIABLE, has no captured value, or the
    value is a dict (which may represent a DataFrame needing a proper Python type).
    """
    if entity.kind != EntityKind.VARIABLE:
        return None
    ab = getattr(entity, "actual_bundle", None)
    if ab is None:
        return None
    name = getattr(entity, "name", None)
    if not name:
        return None
    val = ab.data.get(name) if hasattr(ab, "data") else None
    if val is None:
        return None
    # Skip dicts — they may represent DataFrames or named lists that need proper types
    if isinstance(val, dict):
        return None
    try:
        return f"{name} = {repr(val)}"
    except Exception:
        return None

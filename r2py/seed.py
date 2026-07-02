"""Whole-file seed translation: translate an R script to Python in one LLM call."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from .stage2 import llm as _llm
from .stage2.stitch import (
    build_data_shim,
    collect_shim_needed_names,
    rebuild_entity_line_map,
    remove_shim_overrides,
)
from . import __version__ as _r2py_version

if TYPE_CHECKING:
    from .stage1.script_map import ScriptMap
    from .library import PatternLibrary


_SYSTEM_PROMPT = """\
You are an R-to-Python translator. Translate the given R script into clean, \
idiomatic Python that produces equivalent output.

Rules:
1. Use the standard Python equivalents for R packages (e.g. shiny for Python, \
pandas for data frames, numpy for arrays, plotnine for ggplot2).
2. Do not create stub classes or fake implementations. Use real Python libraries.
3. Drop R documentation scaffolding (withAutoprint, examplesIf, rlang::is_interactive, \
rlang::is_installed wrappers) — translate the actual example code inside them. \
These are guards for optional/interactive examples; in our pipeline the guarded \
code always executes in R, so Python must execute it unconditionally too.
4. When Pattern Library guidance is provided, follow it.
5. In Python, positional arguments must come before keyword arguments in \
every function call. R allows named arguments before positional ones — \
reorder them when translating.
6. Output ONLY the Python code — no explanation, no markdown fences.
"""


def translate(
    script_map: "ScriptMap",
    library: "PatternLibrary",
    *,
    model: str = _llm._DEFAULT_MODEL,
    sidecar_filename: str | None = None,
    script_relpath: str | None = None,
    no_seeds: bool = False,
    r_path: str = "",
) -> tuple[str, dict[str, tuple[int, int]]]:
    """Translate an R script to Python via a single whole-file LLM call.

    Returns (python_source, entity_line_map).
    """
    r_source = script_map.source or ""
    prompt_parts = _build_prompt(script_map, library, no_seeds=no_seeds)
    messages = [{"role": "user", "content": "\n\n".join(prompt_parts)}]

    try:
        raw = _llm.call(messages, _SYSTEM_PROMPT, model=model)
    except Exception as exc:
        print(f"r2py: seed LLM call failed: {exc}", file=sys.stderr)
        raw = "# r2py: seed translation failed"

    python_code = _extract_python(raw)
    python_source = _assemble(
        python_code, script_map, model,
        r_path=r_path,
        sidecar_filename=sidecar_filename,
        script_relpath=script_relpath,
    )
    entity_line_map = rebuild_entity_line_map(python_source)
    return python_source, entity_line_map


def _build_prompt(
    script_map: "ScriptMap",
    library: "PatternLibrary",
    no_seeds: bool = False,
) -> list[str]:
    """Build the user prompt for whole-file translation."""
    from .types import EntityKind

    parts: list[str] = []
    r_source = script_map.source or ""

    parts.append(f"Translate this R script into Python:\n\n```r\n{r_source}\n```")

    # Collect pattern library guidance for entities in this script.
    patterns_seen: set[str] = set()
    pattern_parts: list[str] = []
    entities = getattr(script_map, "entities", {}) or {}
    for entity in entities.values():
        matches = library.retrieve(entity, k=2, no_seeds=no_seeds)
        for pat in matches:
            if pat.id in patterns_seen:
                continue
            patterns_seen.add(pat.id)
            entry = f"**{pat.id}** ({pat.confidence}): {pat.guidance.strip()}"
            for ex in getattr(pat, "translation_examples", [])[:1]:
                entry += (
                    f"\n  R: `{ex.r_snippet[:200]}`"
                    f"\n  Python: `{ex.py_snippet[:300]}`"
                )
            pattern_parts.append(entry)
    if pattern_parts:
        parts.append(
            "## Translation patterns (follow these):\n" + "\n\n".join(pattern_parts)
        )

    # Collect R source lookups for all package symbols referenced by entities.
    imported_pkgs: list[str] = [
        e.package
        for e in entities.values()
        if getattr(e, "kind", None) == EntityKind.LIBRARY_IMPORT and e.package
    ]
    if imported_pkgs:
        source_parts = collect_source_lookups(entities, imported_pkgs)
        if source_parts:
            parts.append(
                "## R function source (for reference — translate the logic, "
                "don't hardcode values):\n" + "\n\n".join(source_parts)
            )

    # Surface resolved_call and function_metadata from Stage 1 probes.
    metadata_text = format_entity_metadata(entities)
    if metadata_text:
        parts.append(
            "## Function metadata (from R introspection):\n" + metadata_text
        )

    return parts


def collect_source_lookups(
    entities: dict,
    imported_pkgs: list[str],
) -> list[str]:
    """Look up R source for all package symbols referenced by entities.

    Collects function names from:
    - entity.name for FUNCTION_CALL and EXTERNAL_SYMBOL entities
    - entity.free_variable_refs for ALL entity kinds (captures nested function
      calls inside assignments, arguments, function bodies, etc.)

    When an entity has entity.package set, looks up source in that specific
    package first before searching all imported packages.
    """
    from .types import EntityKind

    try:
        from .stage1.package_lookup import (
            get_function_source_recursive, _BASE_R_NAMES,
        )
    except ImportError:
        return []

    # Entity names that define local variables/functions — skip these for
    # source lookup since they're script-defined, not package symbols.
    local_defs = {
        eid for eid, e in entities.items()
        if getattr(e, "kind", None) in (
            EntityKind.VARIABLE, EntityKind.FUNCTION_DEF, EntityKind.LIBRARY_IMPORT,
        )
    }
    seen: set[str] = set()
    # (name, packages_to_search) pairs — package-specific lookups first
    lookups: list[tuple[str, list[str]]] = []

    # Collect all identifiers from the script as S3 class hints — when a
    # UseMethod generic is found, only fetch methods whose class suffix
    # matches one of these names (avoids fetching 100+ methods for tidy/glance).
    all_refs: set[str] = set()

    for entity in entities.values():
        kind = getattr(entity, "kind", None)
        all_refs.add(entity.name)

        # For FUNCTION_CALL and EXTERNAL_SYMBOL, the entity name is a function.
        if kind in (EntityKind.FUNCTION_CALL, EntityKind.EXTERNAL_SYMBOL):
            name = entity.name
            if name not in seen and name not in _BASE_R_NAMES:
                seen.add(name)
                pkg = getattr(entity, "package", None)
                if pkg and pkg not in imported_pkgs:
                    lookups.append((name, [pkg] + imported_pkgs))
                else:
                    lookups.append((name, imported_pkgs))

        # For ALL entity kinds, free_variable_refs captures identifiers from
        # RHS expressions / arguments — includes nested function calls.
        for ref in getattr(entity, "free_variable_refs", []):
            all_refs.add(ref)
            if ref not in seen and ref not in local_defs and ref not in _BASE_R_NAMES:
                seen.add(ref)
                lookups.append((ref, imported_pkgs))

    s3_class_hints = frozenset(all_refs)

    parts: list[str] = []
    for name, pkgs in lookups:
        try:
            source = get_function_source_recursive(
                pkgs, name, s3_class_hints=s3_class_hints,
            )
        except Exception:
            source = None
        if source:
            parts.append(f"### `{name}`\n```r\n{source}\n```")
    return parts


def format_entity_metadata(entities: dict) -> str:
    """Format resolved_call and function_metadata for the LLM prompt."""
    parts: list[str] = []
    seen_names: set[str] = set()
    for entity in entities.values():
        name = entity.name
        if name in seen_names:
            continue

        lines: list[str] = []

        resolved = getattr(entity, "resolved_call", None)
        if resolved:
            lines.append(f"  Resolved call: {resolved}")

        fm = getattr(entity, "function_metadata", None)
        if fm:
            if fm.formals:
                formals_str = ", ".join(
                    f"{k}={v}" if v else k
                    for k, v in fm.formals.items()
                )
                lines.append(f"  Formals: {formals_str}")
            if fm.methods:
                lines.append(f"  S3 methods: {', '.join(fm.methods)}")

        if lines:
            seen_names.add(name)
            parts.append(f"  {name}:\n" + "\n".join(lines))

    return "\n".join(parts)


def _extract_python(raw: str) -> str:
    """Extract Python code from LLM response, stripping markdown fences if present."""
    m = re.search(r"```python\s*\n(.*?)```", raw, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"```\s*\n(.*?)```", raw, re.DOTALL)
    if m:
        return m.group(1).strip()
    return raw.strip()


def _assemble(
    python_code: str,
    script_map: "ScriptMap",
    model: str,
    r_path: str = "",
    sidecar_filename: str | None = None,
    script_relpath: str | None = None,
) -> str:
    """Add header, entity sentinels, and data shim to the raw translation."""
    entities = getattr(script_map, "entities", {}) or {}
    n_entities = len(entities)
    r_label = r_path or getattr(script_map, "source_file", "<R script>")

    header = (
        f"# Translated from {r_label} by r2py v{_r2py_version}\n"
        f"# Model: {model}  ScriptMap entities: {n_entities}"
    )

    # Inject entity sentinel comments into the translated code.
    python_code = _inject_sentinels(python_code, script_map)

    # Build data shim if needed.
    shim_needed = collect_shim_needed_names(script_map) if sidecar_filename else []
    shim_text = ""
    if sidecar_filename and shim_needed:
        shim_text = build_data_shim(
            shim_needed, sidecar_filename, script_relpath=script_relpath
        )
        # Strip assignments to shim-loaded names.
        python_code = remove_shim_overrides(python_code, set(shim_needed))

    parts = [header]
    if shim_text:
        parts.append(shim_text)
    parts.append(python_code)

    return "\n\n".join(parts) + "\n"


def _inject_sentinels(python_code: str, script_map: "ScriptMap") -> str:
    """Insert ``# r2py:entity:<id>`` sentinel comments into translated Python.

    Uses heuristic matching: for each entity, look for its name in the Python
    code (as an assignment target, function def, import, or function call) and
    insert the sentinel on the line before the first match.

    Entities that can't be matched get their sentinel appended at the end.
    """
    from .types import EntityKind
    from .stage2.walker import topological_order

    entities = getattr(script_map, "entities", {}) or {}
    if not entities:
        return python_code

    lines = python_code.splitlines()
    order = topological_order(entities)

    # For each entity, find the best matching line.
    # Track which lines already have a sentinel to avoid duplicates.
    sentinel_inserts: dict[int, str] = {}  # line_index -> sentinel text
    matched_eids: set[str] = set()
    claimed_lines: set[int] = set()

    for eid in order:
        entity = entities[eid]
        name = entity.name
        kind = getattr(entity, "kind", None)

        best_line = _find_entity_line(lines, name, kind, claimed_lines)
        if best_line is not None:
            sentinel_inserts[best_line] = f"# r2py:entity:{eid}"
            matched_eids.add(eid)
            claimed_lines.add(best_line)

    # Build result with sentinels inserted before matched lines.
    result: list[str] = []
    for i, line in enumerate(lines):
        if i in sentinel_inserts:
            result.append(sentinel_inserts[i])
        result.append(line)

    # Append unmatched entities at the end.
    unmatched = [eid for eid in order if eid not in matched_eids]
    if unmatched:
        for eid in unmatched:
            result.append(f"# r2py:entity:{eid}")

    return "\n".join(result)


_IMPORT_RE = re.compile(r"^\s*(?:import|from)\s+")


def _find_entity_line(
    lines: list[str],
    name: str,
    kind,
    claimed: set[int],
) -> int | None:
    """Find the line index where entity *name* first appears in *lines*."""
    from .types import EntityKind

    if not name:
        return None

    # Normalize: R uses . in names, Python uses _
    py_name = name.replace(".", "_").replace("::", ".")
    # Also try the raw name for exact matches
    candidates = {py_name}
    if py_name != name:
        candidates.add(name)

    # For function defs, look for `def name(`
    if kind == EntityKind.FUNCTION_DEF:
        for i, line in enumerate(lines):
            if i in claimed:
                continue
            for n in candidates:
                if re.search(rf"^\s*def\s+{re.escape(n)}\s*\(", line):
                    return i
        # Fall through to general search

    # For library imports, look for import statements
    if kind == EntityKind.LIBRARY_IMPORT:
        for i, line in enumerate(lines):
            if i in claimed:
                continue
            if not _IMPORT_RE.match(line):
                continue
            for n in candidates:
                if n in line:
                    return i
        return None

    # For variables, look for `name = ` assignment
    if kind == EntityKind.VARIABLE:
        for i, line in enumerate(lines):
            if i in claimed:
                continue
            for n in candidates:
                if re.search(rf"^{re.escape(n)}\s*=(?!=)", line):
                    return i
        # Fall through

    # General: look for the name in any context
    for i, line in enumerate(lines):
        if i in claimed:
            continue
        for n in candidates:
            if re.search(rf"\b{re.escape(n)}\b", line):
                return i

    return None

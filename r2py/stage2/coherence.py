"""Whole-program coherence review pass for Stage 2 (§5.6).

One LLM call over the full stitched Python file.  May only emit typed edits
(§8.3) — never a free rewrite — so it cannot destroy already-correct work.
On any failure returns the original source unchanged.
"""
from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING

from . import llm as _llm

if TYPE_CHECKING:
    from ..stage1.script_map import ScriptMap
    from ..library import PatternLibrary
    from ..types import Edit

from ..types import Edit, EditKind

_COHERENCE_SYSTEM = """\
You are reviewing a complete Python translation of an R script for global coherence.
Your job is to catch inter-entity problems invisible to any single entity's translator:
inconsistent variable types, broken dataflow assumptions, import conflicts, and
emergent interactions from composition.

You may ONLY suggest these specific types of changes (never a free rewrite):
  - InsertPreamble   : insert code either at the very top of the file
                        (entity_ids: []) OR at the top of one or more specific
                        entity bodies (entity_ids: ["eid", ...]). Use the
                        entity-scoped form to DEFINE NAMES THAT AN ENTITY USES
                        BUT COULD NOT DEFINE ITSELF — most importantly,
                        R built-in datasets like `volcano`, `mtcars`, `iris`,
                        `Titanic`, `airquality`. The per-entity translator
                        often leaves a placeholder + a comment such as
                        "# Placeholder; actual <name> data would be loaded";
                        when you see that, replace the placeholder by inserting
                        the real definition (or a load call) at the top of the
                        entity's body.
  - RenameVariable   : rename a variable name consistently throughout
  - ChangeImport     : replace one import statement with another
  - WrapValue        : wrap a value in a conversion call (e.g. str(x), int(x))
  - ReplaceCall      : replace one function call with another

For each suggested change output exactly ONE JSON object on its own line.
If there are no changes needed, output nothing at all.
Use this schema (no prose, no extra text on these lines):
{"kind": "RenameVariable", "entity_ids": ["x"], "params": {"old": "foo", "new": "bar"}}
{"kind": "InsertPreamble", "entity_ids": [], "params": {"code": "import numpy as np"}}
{"kind": "InsertPreamble", "entity_ids": ["filled.contour"], "params": {"code": "volcano = [[...real 87x61 values...]]"}}
{"kind": "ChangeImport", "entity_ids": [], "params": {"old_import": "import pandas", "new_import": "import pandas as pd"}}
{"kind": "WrapValue", "entity_ids": ["x"], "params": {"name": "result", "wrapper": "str"}}
{"kind": "ReplaceCall", "entity_ids": ["x"], "params": {"old_call": "foo(x)", "new_call": "bar(x)"}}

Choosing between InsertPreamble (entity-scoped) and ReplaceCall when a
placeholder is in the way:

1. If the entity body has NO assignment to the name yet (the entity just
   references it as a free name), use InsertPreamble with entity_ids targeting
   that entity to introduce the definition.

2. If the entity body ALREADY assigns the name to a placeholder value
   (typical pattern: a comment like "# Placeholder; actual <name> would be
   loaded" followed by something like
        volcano_data = np.array([[94, 94, ...], [94, 94, ...]])
   ), entity-scoped InsertPreamble will be SKIPPED because the name is
   already bound. Use ReplaceCall instead, passing the EXACT placeholder
   right-hand side as old_call and the real value as new_call:
     {"kind": "ReplaceCall", "entity_ids": ["filled.contour"],
      "params": {"old_call": "np.array([[94, 94, ...], [94, 94, ...]])",
                 "new_call": "np.array([[<real 87x61 values>]])"}}
   ReplaceCall is a plain text replace, so old_call must match the literal in
   the source character-for-character (including newlines and indentation).

3. If the placeholder was given a renamed Python name (e.g. R's `volcano`
   became `volcano_data` in the per-entity output), do NOT inject the data at
   the file top under the R name — that produces dead code. Either keep the
   renamed name and ReplaceCall its RHS, or RenameVariable everything back to
   the R name first and then InsertPreamble.

## SHIM-LOADED NAMES (CRITICAL)

The user message may include a section "## Shim-loaded names" listing names
that are pre-bound into module globals by a data-loading shim BEFORE the body
runs.  For each such name:

  - Do NOT emit InsertPreamble whose `code` assigns it.
  - Do NOT emit ReplaceCall whose `new_call` binds it via an assignment.
  - Do NOT emit RenameVariable that renames such a name (the shim references
    it by its original name).

The shim's value is authoritative — any binding edit you emit will be
stripped post-coherence anyway, wasting an LLM round-trip.  If you see a
placeholder for a shim-loaded name (e.g. ``volcano = np.array([[94, 94, ...]])``),
the right action is to leave it alone or RemoveLine it (use ReplaceCall with
new_call="" to delete it).

## LIBRARY FUNCTION REFERENCES

Check that free variable refs from loaded R packages are properly wired up.
A common failure mode: entity A's R source passes a library function by
reference (e.g. ``filled.contour(volcano, color = graycol, ...)`` where
``graycol`` is a function from ``library(shape)``), but the per-entity
translator didn't know what ``graycol`` was and substituted a built-in
fallback (e.g. ``cmap='gray'``).  Meanwhile, a later entity B correctly
defines ``graycol()`` as a Python function.

When you see this pattern — a Python function defined by one entity but not
used by an earlier entity that should reference it — emit a ReplaceCall to
wire them up.  For example:
{"kind": "ReplaceCall", "entity_ids": ["filled.contour"], "params": {"old_call": "cmap='gray'", "new_call": "colors=graycol()"}}

Check the entity summary's ``free_vars`` lists: if an entity lists a free
variable that matches the name of a function defined by another entity,
verify the translation actually uses that function.
"""


def review(
    python_source: str,
    script_map: "ScriptMap",
    library: "PatternLibrary",
    model: str = _llm._DEFAULT_MODEL,
    shim_names: list[str] | None = None,
) -> tuple[str, list["Edit"]]:
    """Run the whole-program coherence pass.

    Returns (revised_python_source, list_of_edits).
    On any failure returns (python_source, []) — the pass can never lower the score.

    shim_names: names pre-bound into module globals by the data-loading shim
    (Option A).  Surfaced in the user message so the LLM skips edits that
    re-bind them; a post-pass in translator.translate() strips any that slip
    through.
    """
    if not python_source.strip():
        return python_source, []

    try:
        user_content = _build_user_message(python_source, script_map, shim_names)
        messages = [{"role": "user", "content": user_content}]
        raw = _llm.call(messages, _COHERENCE_SYSTEM, model=model)
        revised, edits = _parse_response(raw, python_source)
        revised = _hoist_imports(revised)
        return revised, edits
    except Exception:
        return python_source, []


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_IMPORT_RE = re.compile(
    r"^(?:import\s|from\s\S+\s+import\s)", re.MULTILINE
)
_COMMENT_OR_BLANK_RE = re.compile(r"^(\s*#.*|\s*)$")
_SENTINEL_RE = re.compile(r"^# r2py:entity:\S+$")


def _hoist_imports(source: str) -> str:
    """Move import statements to the top if code precedes them.

    Scans for lines that are import statements. If any non-import,
    non-comment, non-blank, non-sentinel code appears *before* the first
    import, all import lines are collected, removed from their original
    positions, and re-inserted at the top of the file. The code that was
    originally above the imports follows immediately after.
    """
    lines = source.splitlines(keepends=True)
    if not lines:
        return source

    import_indices: list[int] = []
    first_import_idx: int | None = None
    has_code_before_first_import = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        if _IMPORT_RE.match(stripped):
            import_indices.append(i)
            if first_import_idx is None:
                first_import_idx = i
        elif first_import_idx is None and not _COMMENT_OR_BLANK_RE.match(stripped) and not _SENTINEL_RE.match(stripped):
            has_code_before_first_import = True

    if not has_code_before_first_import or not import_indices:
        return source

    import_lines = [lines[i] for i in import_indices]
    remaining = [lines[i] for i in range(len(lines)) if i not in set(import_indices)]

    # Ensure each import line ends with a newline
    import_lines = [l if l.endswith("\n") else l + "\n" for l in import_lines]

    return "".join(import_lines) + "".join(remaining)


def _build_user_message(
    python_source: str,
    script_map: "ScriptMap",
    shim_names: list[str] | None = None,
) -> str:
    entity_summary = _summarise_entities(script_map)
    shim_block = ""
    if shim_names:
        names_str = ", ".join(f"`{n}`" for n in sorted(shim_names))
        shim_block = (
            "## Shim-loaded names\n"
            f"The following names are pre-bound into module globals by the "
            f"data-loading shim before the body runs: {names_str}.\n"
            "Do NOT emit InsertPreamble/ReplaceCall/RenameVariable edits that "
            "re-bind or rename these names. The shim's values are authoritative; "
            "any such edits will be stripped post-coherence.\n\n"
        )
    return (
        "## Python translation to review\n"
        f"```python\n{python_source}\n```\n\n"
        f"{shim_block}"
        "## ScriptMap entity summary (for cross-entity coherence check)\n"
        f"{entity_summary}\n\n"
        "Review the Python translation for global coherence issues. "
        "Output edit JSON lines (if any), then the full revised source in <python>...</python> tags."
    )


def _summarise_entities(script_map: "ScriptMap") -> str:
    if not hasattr(script_map, "entities") or not script_map.entities:
        return "(no entity information)"
    lines: list[str] = []
    source_lines = (script_map.source or "").splitlines() if hasattr(script_map, "source") else []
    for eid, entity in script_map.entities.items():
        flags = ", ".join(entity.r_semantic_flags) or "none"
        effects = ", ".join(
            getattr(e, "value", str(e)) for e in entity.predicted_effects
        ) or "none"
        pkg = getattr(entity, "package", None)
        pkg_str = f"  package={pkg}" if pkg else ""

        # R source snippet for this entity
        r_src = ""
        sp = getattr(entity, "source_span", None)
        if sp is not None and source_lines:
            start = getattr(sp, "start_line", 0)
            end = min(len(source_lines), getattr(sp, "end_line", start) + 1)
            snippet = "\n    ".join(source_lines[start:end])
            r_src = f"  R: {snippet}"

        # Free variables (built-in datasets, package-namespace names, etc.)
        free_refs = getattr(entity, "free_variable_refs", [])
        free_str = f"  free_vars=[{', '.join(free_refs)}]" if free_refs else ""

        lines.append(
            f"- {eid} ({_kind_str(entity)}):{pkg_str}  flags=[{flags}]"
            f"  effects=[{effects}]{free_str}{('  ' + r_src) if r_src else ''}"
        )
    return "\n".join(lines)


def _kind_str(entity: object) -> str:
    kind = getattr(entity, "kind", None)
    return getattr(kind, "value", str(kind)) if kind is not None else "unknown"


def _parse_response(raw: str, original: str) -> tuple[str, list["Edit"]]:
    """Extract typed edits (JSON lines) from the LLM response and apply them.

    The <python> block from the LLM is ignored — the revised source is produced
    by applying each typed edit programmatically to the original.  This enforces
    the §5.6 constraint that the coherence pass "may only emit typed edits —
    never a free rewrite": the edit taxonomy is the only mutation path.
    """
    edits: list[Edit] = []

    # Collect JSON lines from anywhere in the response (before or after <python>)
    python_match = re.search(r"<python>(.*?)</python>", raw, re.DOTALL)
    # Scan the part of the response before <python> for edit JSON lines
    scan_text = raw[: python_match.start()] if python_match else raw

    for line in scan_text.splitlines():
        line = line.strip()
        if not (line.startswith("{") and line.endswith("}")):
            continue
        try:
            obj = json.loads(line)
            edit = _json_to_edit(obj)
            if edit is not None:
                edits.append(edit)
        except (json.JSONDecodeError, KeyError, ValueError):
            continue

    # Apply each typed edit to the original source programmatically.
    revised = original
    for edit in edits:
        revised = _apply_edit(revised, edit)

    return revised, edits


def _apply_edit(source: str, edit: "Edit") -> str:
    """Apply one typed edit to a Python source string.

    Covers the edit kinds the coherence pass naturally produces (§8.3):
      INSERT_PREAMBLE  — prepend code before the first non-comment/non-blank line.
      RENAME_VARIABLE  — whole-word replace params["old"] → params["new"].
      CHANGE_IMPORT    — line-level replace of params["old_import"] line.
      WRAP_VALUE       — surround all occurrences of a name with wrapper(name).
      REPLACE_CALL     — plain text replace of params["old_call"] → params["new_call"].
    Other kinds are silently ignored (they belong to Stage 3).
    """
    p = edit.params
    try:
        if edit.kind == EditKind.INSERT_PREAMBLE:
            code = p.get("code", "").strip()
            if not code:
                return source
            # Delegate to the canonical applier so file-top vs entity-scoped
            # behaviour stays consistent with Stage 3.
            from ..stage3.edit_types import apply_edit as _apply_edit_canonical
            return _apply_edit_canonical(source, edit)

        elif edit.kind == EditKind.RENAME_VARIABLE:
            old, new = p.get("old", ""), p.get("new", "")
            if not old or not new:
                return source
            return re.sub(rf"\b{re.escape(old)}\b", new, source)

        elif edit.kind == EditKind.CHANGE_IMPORT:
            old_imp = p.get("old_import", "").strip()
            new_imp = p.get("new_import", "").strip()
            if not old_imp:
                return source
            lines = source.splitlines(keepends=True)
            result = []
            for line in lines:
                if line.strip() == old_imp:
                    result.append(new_imp + "\n")
                else:
                    result.append(line)
            return "".join(result)

        elif edit.kind == EditKind.WRAP_VALUE:
            name = p.get("name", "")
            wrapper = p.get("wrapper", "")
            if not name or not wrapper:
                return source
            return re.sub(rf"\b{re.escape(name)}\b", f"{wrapper}({name})", source)

        elif edit.kind == EditKind.REPLACE_CALL:
            old_call = p.get("old_call", "")
            new_call = p.get("new_call", "")
            if not old_call:
                return source
            return source.replace(old_call, new_call)

    except Exception:
        pass  # bad params — leave source unchanged

    return source


def _json_to_edit(obj: dict) -> "Edit | None":
    """Convert a parsed JSON dict to an Edit, returning None if kind is unknown."""
    kind_str = obj.get("kind", "")
    try:
        kind = EditKind(kind_str)
    except ValueError:
        return None
    entity_ids = obj.get("entity_ids", [])
    params = obj.get("params", {})
    return Edit(kind=kind, entity_ids=entity_ids, params=params, pattern_id=None)

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
  - InsertPreamble   : add an import or initialisation line at the very top
  - RenameVariable   : rename a variable name consistently throughout
  - ChangeImport     : replace one import statement with another
  - WrapValue        : wrap a value in a conversion call (e.g. str(x), int(x))
  - ReplaceCall      : replace one function call with another

For each suggested change output exactly ONE JSON object on its own line.
If there are no changes needed, output nothing at all.
Use this schema (no prose, no extra text on these lines):
{"kind": "RenameVariable", "entity_ids": ["x"], "params": {"old": "foo", "new": "bar"}}
{"kind": "InsertPreamble", "entity_ids": [], "params": {"code": "import numpy as np"}}
{"kind": "ChangeImport", "entity_ids": [], "params": {"old_import": "import pandas", "new_import": "import pandas as pd"}}
{"kind": "WrapValue", "entity_ids": ["x"], "params": {"name": "result", "wrapper": "str"}}
{"kind": "ReplaceCall", "entity_ids": ["x"], "params": {"old_call": "foo(x)", "new_call": "bar(x)"}}
"""


def review(
    python_source: str,
    script_map: "ScriptMap",
    library: "PatternLibrary",
    model: str = _llm._DEFAULT_MODEL,
) -> tuple[str, list["Edit"]]:
    """Run the whole-program coherence pass.

    Returns (revised_python_source, list_of_edits).
    On any failure returns (python_source, []) — the pass can never lower the score.
    """
    if not python_source.strip():
        return python_source, []

    try:
        user_content = _build_user_message(python_source, script_map)
        messages = [{"role": "user", "content": user_content}]
        raw = _llm.call(messages, _COHERENCE_SYSTEM, model=model)
        return _parse_response(raw, python_source)
    except Exception:
        return python_source, []


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _build_user_message(python_source: str, script_map: "ScriptMap") -> str:
    entity_summary = _summarise_entities(script_map)
    return (
        "## Python translation to review\n"
        f"```python\n{python_source}\n```\n\n"
        "## ScriptMap entity summary (for cross-entity coherence check)\n"
        f"{entity_summary}\n\n"
        "Review the Python translation for global coherence issues. "
        "Output edit JSON lines (if any), then the full revised source in <python>...</python> tags."
    )


def _summarise_entities(script_map: "ScriptMap") -> str:
    if not hasattr(script_map, "entities") or not script_map.entities:
        return "(no entity information)"
    lines: list[str] = []
    for eid, entity in script_map.entities.items():
        flags = ", ".join(entity.r_semantic_flags) or "none"
        effects = ", ".join(
            getattr(e, "value", str(e)) for e in entity.predicted_effects
        ) or "none"
        lines.append(f"- {eid} ({_kind_str(entity)}): flags=[{flags}]  effects=[{effects}]")
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
            lines = source.splitlines(keepends=True)
            insert_at = 0
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped and not stripped.startswith("#"):
                    insert_at = i
                    break
            lines.insert(insert_at, code + "\n")
            return "".join(lines)

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

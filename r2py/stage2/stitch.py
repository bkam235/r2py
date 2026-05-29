"""Compose per-entity Python snippets into one .py file (§5.5)."""
from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .. import __version__ as _r2py_version

if TYPE_CHECKING:
    from ..stage1.script_map import ScriptMap
    from ..types import EntityId


def compose(
    per_entity: dict[str, str],
    per_entity_imports: dict[str, list[str]],
    order: list[str],
    script_map: "ScriptMap",
    model: str,
    r_path: str = "",
) -> str:
    """Compose ordered snippets into a single Python source string.

    Steps:
    1. Collect all import lines (from snippets + per_entity_imports), deduplicate, sort.
    2. Collect body snippets in topological order.
    3. Resolve name collisions (suffix _1, _2, ...).
    4. Prepend header comment.
    """
    all_imports: list[str] = []
    body_snippets: list[str] = []
    defined_names: dict[str, str] = {}  # python_name → entity_id that defined it

    for eid in order:
        snippet = per_entity.get(eid, "")
        # Collect explicit imports registered by the translator
        for imp in per_entity_imports.get(eid, []):
            imp = imp.strip()
            if imp and _is_import_line(imp):
                all_imports.append(imp)

        # Split snippet into import lines vs body lines
        imp_lines, body_lines = _split_imports(snippet)
        all_imports.extend(imp_lines)

        if body_lines:
            # Rename collision: check top-level assigned names
            body_text = "\n".join(body_lines)
            body_text = _resolve_collisions(body_text, eid, defined_names)
            body_snippets.append(body_text)

    # Deduplicate and sort imports
    seen: set[str] = set()
    deduped_imports: list[str] = []
    for imp in all_imports:
        if imp not in seen:
            seen.add(imp)
            deduped_imports.append(imp)
    deduped_imports.sort(key=_import_sort_key)

    # Build header
    n_entities = len(script_map.entities) if hasattr(script_map, "entities") else 0
    r_label = r_path or getattr(script_map, "source_file", "<R script>")
    header = (
        f"# Translated from {r_label} by r2py v{_r2py_version}\n"
        f"# Model: {model}  ScriptMap entities: {n_entities}"
    )

    # Assemble
    parts: list[str] = [header]
    if deduped_imports:
        parts.append("\n".join(deduped_imports))
    if body_snippets:
        parts.append("\n\n".join(body_snippets))

    return "\n\n".join(parts) + "\n"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_IMPORT_RE = re.compile(r"^\s*(import |from \S+ import )")


def _is_import_line(line: str) -> bool:
    return bool(_IMPORT_RE.match(line))


def _split_imports(snippet: str) -> tuple[list[str], list[str]]:
    """Split a snippet into (import lines, non-import lines)."""
    imports: list[str] = []
    body: list[str] = []
    for line in snippet.splitlines():
        if _is_import_line(line):
            imports.append(line.strip())
        else:
            body.append(line)
    # Strip leading/trailing blank lines from body
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    return imports, body


def _import_sort_key(imp: str) -> tuple[int, str]:
    """Sort: bare 'import X' before 'from X import Y', then alphabetically."""
    is_from = imp.startswith("from ")
    return (int(is_from), imp.lower())


_ASSIGN_RE = re.compile(r"^(\s*)([A-Za-z_]\w*)\s*=(?!=)")


def _resolve_collisions(
    body: str,
    eid: str,
    defined_names: dict[str, str],
) -> str:
    """Suffix top-level assigned names that clash with already-defined ones."""
    lines = body.splitlines()
    renames: dict[str, str] = {}

    for line in lines:
        m = _ASSIGN_RE.match(line)
        if not m:
            continue
        indent, name = m.group(1), m.group(2)
        if indent:  # only top-level (no indentation)
            continue
        if name in defined_names and defined_names[name] != eid:
            suffix = 1
            new_name = f"{name}_{suffix}"
            while new_name in defined_names:
                suffix += 1
                new_name = f"{name}_{suffix}"
            renames[name] = new_name
        else:
            defined_names[name] = eid

    if not renames:
        return body

    # Apply renames as whole-word replacements
    result = body
    for old, new in renames.items():
        result = re.sub(rf"\b{re.escape(old)}\b", new, result)
        defined_names[new] = eid
    return result

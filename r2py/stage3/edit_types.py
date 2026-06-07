"""Canonical apply_edit() for all 7 EditKind cases (§8.3).

Also provides edit_to_dict / dict_to_edit helpers used by the prompt
parser and the edit log writer.
"""
from __future__ import annotations

import re

from ..types import Edit, EditKind


_SENTINEL_PREFIX = "# r2py:entity:"


def _find_entity_body(source: str, eid: str) -> tuple[int, int] | None:
    """Return 0-indexed (insert_idx, end_idx) where the entity body lives.

    insert_idx is the line immediately after the `# r2py:entity:<eid>` sentinel
    (i.e. the top of the body). end_idx is the line of the next sentinel or
    len(lines). Returns None when the sentinel is not present.
    """
    sentinel = _SENTINEL_PREFIX + eid
    lines = source.splitlines(keepends=True)
    start: int | None = None
    for i, line in enumerate(lines):
        if line.rstrip("\n") == sentinel:
            start = i + 1
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith(_SENTINEL_PREFIX):
            end = j
            break
    return start, end


def _insert_into_entity_bodies(source: str, eids: list[str], code: str) -> str:
    """Insert ``code`` at the top of each entity body referenced in ``eids``.

    Per-entity dedup: when ``code`` defines a name the entity body already
    binds, the insertion is skipped for that entity. The LLM is expected to
    use ``ReplaceCall`` to swap a placeholder literal directly when it wants
    to override a per-entity assignment.
    """
    defined = set(re.findall(r'^(?:def |class )(\w+)\s*[\(:]', code, re.MULTILINE))
    defined |= set(re.findall(r'^(\w+)\s*=', code, re.MULTILINE))

    lines = source.splitlines(keepends=True)
    spans: list[tuple[int, int, str]] = []
    for eid in eids:
        span = _find_entity_body("".join(lines), eid)
        if span is None:
            continue
        start, end = span
        body_text = "".join(lines[start:end])
        already_has = any(
            re.search(rf'^(?:def |class ){re.escape(n)}\b', body_text, re.MULTILINE)
            or re.search(rf'^{re.escape(n)}\s*=', body_text, re.MULTILINE)
            for n in defined
        )
        if already_has:
            continue
        spans.append((start, end, eid))

    for start, _end, _eid in sorted(spans, key=lambda s: s[0], reverse=True):
        lines.insert(start, code + "\n")
    return "".join(lines)


def apply_edit(source: str, edit: Edit) -> str:
    """Apply one typed edit to a Python source string.

    All 7 EditKind cases are handled. On bad params or any exception the
    original source is returned unchanged.
    """
    p = edit.params
    try:
        if edit.kind == EditKind.INSERT_PREAMBLE:
            code = p.get("code", "").strip()
            if not code:
                return source
            # When entity_ids is non-empty, insert at the top of each named
            # entity's body (right after the `# r2py:entity:<eid>` sentinel).
            # Use this to define names the entity references but cannot define
            # itself (e.g. R built-in datasets like `volcano`, `mtcars`).
            if edit.entity_ids:
                return _insert_into_entity_bodies(source, list(edit.entity_ids), code)
            # File-top preamble (original behaviour).
            # Dedup: skip if any top-level name defined by the preamble already
            # exists in the source.  Prevents _with_locale / _LOCALE_MAP from
            # being re-inserted for every with_locale_N entity.
            defined = set(re.findall(r'^(?:def |class )(\w+)\s*[\(:]', code, re.MULTILINE))
            defined |= set(re.findall(r'^(\w+)\s*=', code, re.MULTILINE))
            for name in defined:
                if re.search(rf'^(?:def |class ){re.escape(name)}\b', source, re.MULTILINE):
                    return source
                if re.search(rf'^{re.escape(name)}\s*=', source, re.MULTILINE):
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

        elif edit.kind == EditKind.RESTRUCTURE_CONTROL_FLOW:
            old_code = p.get("old_code", "")
            new_code = p.get("new_code", "")
            if not old_code:
                return source
            return source.replace(old_code, new_code)

        elif edit.kind == EditKind.RETRANSLATE_ENTITY:
            new_snippet = p.get("new_snippet", "").strip()
            if not new_snippet:
                return source
            stub = "pass  # r2py: translation failed for entity (LLM response not valid Python)"
            if stub not in source:
                return source
            return source.replace(stub, new_snippet, 1)

        elif edit.kind == EditKind.REPLACE_LIBRARY:
            old_name = p.get("old_name", "")
            new_name = p.get("new_name", "")
            old_import = p.get("old_import", "").strip()
            new_import = p.get("new_import", "").strip()
            if not old_name or not new_name:
                return source
            # Replace name references on non-import lines first, then swap the
            # import line.  Doing it this way prevents the name regex from
            # accidentally mangling the new import line (e.g. if new_import
            # itself contains old_name as a substring of a new alias).
            lines = source.splitlines(keepends=True)
            result_lines = []
            for line in lines:
                if old_import and line.strip() == old_import:
                    result_lines.append(new_import + "\n" if new_import else line)
                else:
                    result_lines.append(
                        re.sub(rf"\b{re.escape(old_name)}\b", new_name, line)
                    )
            return "".join(result_lines)

    except Exception:
        pass

    return source


def edit_to_dict(edit: Edit) -> dict:
    """Serialise an Edit to a plain dict (for JSON logging and prompt embedding)."""
    return {
        "kind": edit.kind.value,
        "entity_ids": list(edit.entity_ids),
        "params": dict(edit.params),
        "pattern_id": edit.pattern_id,
    }


def dict_to_edit(d: dict) -> Edit:
    """Deserialise a plain dict to an Edit.

    Raises ValueError if 'kind' is missing or not a valid EditKind.
    """
    kind = EditKind(d["kind"])
    return Edit(
        kind=kind,
        entity_ids=list(d.get("entity_ids", [])),
        params=dict(d.get("params", {})),
        pattern_id=d.get("pattern_id"),
        guidance=str(d.get("guidance", "")),
    )

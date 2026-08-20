"""LLM-based entity-to-Python-line mapping for verification scoring."""
from __future__ import annotations

import json
import re

from . import llm as _llm

_SENTINEL_RE = re.compile(r"^# r2py:entity:\S+$")


class SentinelMappingError(RuntimeError):
    """Raised when the LLM fails to produce a valid entity-line mapping."""


def strip_sentinels(python_source: str) -> str:
    """Remove all ``# r2py:entity:<id>`` lines from Python source."""
    return "\n".join(
        line for line in python_source.splitlines()
        if not _SENTINEL_RE.match(line)
    )


def insert_sentinels(
    python_source: str,
    entity_line_map: "dict[str, list[tuple[int, int]]] | dict[str, tuple[int, int]]",
) -> str:
    """Insert ``# r2py:entity:<id>`` comments at mapped start lines.

    Accepts both multi-range (list of (start, end)) and single-range (start, end)
    values.  Line numbers are 1-based inclusive.  The sentinel is inserted on its
    own line immediately before each range's start line.
    """
    lines = python_source.splitlines()
    inserts: list[tuple[int, str]] = []
    for eid, ranges in entity_line_map.items():
        if isinstance(ranges, list):
            for (start, _end) in ranges:
                inserts.append((start, f"# r2py:entity:{eid}"))
        else:
            inserts.append((ranges[0], f"# r2py:entity:{eid}"))
    inserts.sort(key=lambda x: x[0])

    result: list[str] = []
    insert_idx = 0
    for i, line in enumerate(lines, start=1):
        while insert_idx < len(inserts) and inserts[insert_idx][0] == i:
            result.append(inserts[insert_idx][1])
            insert_idx += 1
        result.append(line)
    while insert_idx < len(inserts):
        result.append(inserts[insert_idx][1])
        insert_idx += 1
    return "\n".join(result)


def flatten_entity_line_map(
    multi_map: "dict[str, list[tuple[int, int]]]",
) -> "dict[str, tuple[int, int]]":
    """Flatten a multi-range entity map to single-range (last range per entity).

    The last range is the call site / assignment — the part that produces
    observable effects for verification.  Function definitions (earlier ranges)
    are setup code with no direct effects.
    """
    return {eid: ranges[-1] for eid, ranges in multi_map.items() if ranges}


_SYSTEM_PROMPT = """\
You map R code entities to their Python translation lines. \
Return ONLY a JSON array — no explanation, no markdown fences."""

_USER_TEMPLATE = """\
## R entities (in execution order)
{entity_listing}

## Python translation (line numbers shown)
{python_listing}

## Task
For each R entity above, identify which Python lines implement it.

Rules:
- A FunctionCall entity (e.g. `tidy(dw)`) owns BOTH the Python function \
definition that implements the R function AND the call site(s) where it is \
invoked. Emit one entry per contiguous block (the same entity_id may appear \
more than once).
- A Variable entity (e.g. `dw <- durbinWatsonTest(...)`) owns the Python \
function/class definitions that implement the R function it calls, PLUS the \
code that computes and assigns its value (model fitting, setup steps, the \
assignment itself). Again, one entry per contiguous block.
- A LibraryImport entity (library/require call) should be OMITTED — the \
function definitions belong to the FunctionCall or Variable entity that uses \
them, not to the import.
- Top-level import statements (import numpy, etc.) belong to no entity — \
omit them.
- If an R entity has no distinct Python lines (e.g. a wrapper like \
suppressPackageStartupMessages), OMIT it from the array.
- The same entity_id MAY appear multiple times (once per contiguous block).
- Line ranges must not overlap across different entities.
- Lines not covered by any entity are fine (imports, blank lines, comments).
- start_line and end_line are 1-based and inclusive.

Return ONLY a JSON array (no other text):
[{{"entity_id": "...", "start_line": N, "end_line": M}}, ...]"""


def _build_entity_listing(script_map) -> str:
    entities = getattr(script_map, "entities", {})
    source = getattr(script_map, "source", "") or ""
    source_lines = source.splitlines()

    from .walker import topological_order
    order = topological_order(entities)

    parts: list[str] = []
    for eid in order:
        entity = entities[eid]
        kind = getattr(getattr(entity, "kind", None), "value", "?")
        span = getattr(entity, "source_span", None)
        r_snip = ""
        if span and source_lines:
            start = getattr(span, "start_line", 0)
            end = min(len(source_lines), getattr(span, "end_line", start) + 1)
            r_snip = "\n".join(source_lines[start:end])[:300]
        parts.append(f'Entity "{eid}" ({kind}):\n  R source: {r_snip}')
    return "\n\n".join(parts)


def _build_python_listing(python_source: str) -> str:
    lines = python_source.splitlines()
    width = len(str(len(lines)))
    return "\n".join(f"{i:{width}d}: {line}" for i, line in enumerate(lines, 1))


def _parse_response(
    raw: str, entity_ids: set[str], total_lines: int,
) -> dict[str, list[tuple[int, int]]]:
    raw = raw.strip()
    if raw.startswith("```"):
        m = re.search(r"```(?:json)?\s*\n(.*?)```", raw, re.DOTALL)
        if m:
            raw = m.group(1).strip()

    try:
        items = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SentinelMappingError(f"LLM returned invalid JSON: {exc}") from exc

    if not isinstance(items, list):
        raise SentinelMappingError(f"Expected JSON array, got {type(items).__name__}")

    result: dict[str, list[tuple[int, int]]] = {}
    all_ranges: list[tuple[str, int, int]] = []
    for item in items:
        if not isinstance(item, dict):
            raise SentinelMappingError(f"Expected object in array, got {type(item).__name__}")
        eid = item.get("entity_id", "")
        start = item.get("start_line")
        end = item.get("end_line")
        if not eid or start is None or end is None:
            raise SentinelMappingError(f"Missing fields in mapping: {item}")
        if eid not in entity_ids:
            raise SentinelMappingError(f"Unknown entity_id: {eid}")
        if not isinstance(start, int) or not isinstance(end, int):
            raise SentinelMappingError(f"Non-integer line numbers for {eid}: {start}, {end}")
        if start < 1 or end > total_lines or start > end:
            raise SentinelMappingError(
                f"Invalid line range for {eid}: {start}-{end} (file has {total_lines} lines)"
            )
        result.setdefault(eid, []).append((start, end))
        all_ranges.append((eid, start, end))

    # Resolve cross-entity overlaps: sort by start line, then clip each range so
    # it ends just before the next one starts.  This handles the common failure
    # where a small-model maps a helper entity (e.g. is_installed) to a huge
    # range that spans later entities.  If clipping makes a range invalid
    # (start > end) it is dropped.  Only raise if the LLM response was so
    # broken that we'd end up with zero valid ranges.
    all_ranges.sort(key=lambda x: x[1])
    overlaps_fixed = False
    for i in range(len(all_ranges) - 1):
        eid_a, start_a, end_a = all_ranges[i]
        eid_b, start_b, _ = all_ranges[i + 1]
        if end_a >= start_b:
            new_end_a = start_b - 1
            all_ranges[i] = (eid_a, start_a, new_end_a)
            overlaps_fixed = True

    if overlaps_fixed:
        result = {}
        for eid, start, end in all_ranges:
            if end >= start:
                result.setdefault(eid, []).append((start, end))
        if not result:
            raise SentinelMappingError(
                "All entity ranges were eliminated while resolving overlaps"
            )

    return result


def map_entities_to_lines(
    script_map,
    python_source: str,
    *,
    model: str,
) -> dict[str, list[tuple[int, int]]]:
    """Call the LLM to map R entities to Python line ranges.

    Returns dict[entity_id, [(start, end), ...]] with 1-based inclusive lines.
    A single entity may own multiple non-contiguous ranges (e.g. a function
    definition and its call site).
    Raises SentinelMappingError on failure.
    """
    clean = strip_sentinels(python_source)
    entities = getattr(script_map, "entities", {})
    if not entities:
        return {}

    entity_listing = _build_entity_listing(script_map)
    python_listing = _build_python_listing(clean)
    total_lines = len(clean.splitlines())
    entity_ids = set(entities.keys())

    user_msg = _USER_TEMPLATE.format(
        entity_listing=entity_listing,
        python_listing=python_listing,
    )

    messages = [{"role": "user", "content": user_msg}]

    raw = _llm.call(messages, system=_SYSTEM_PROMPT, model=model, max_tokens=2048)

    try:
        return _parse_response(raw, entity_ids, total_lines)
    except SentinelMappingError as first_err:
        retry_messages = messages + [
            {"role": "assistant", "content": raw},
            {"role": "user", "content": (
                f"Error: {first_err}\n\n"
                "Fix the problem and return the corrected JSON array. "
                "Remember: ranges must not overlap, and entities with no "
                "distinct Python lines should be omitted."
            )},
        ]
        raw2 = _llm.call(
            retry_messages, system=_SYSTEM_PROMPT, model=model, max_tokens=2048,
        )
        return _parse_response(raw2, entity_ids, total_lines)

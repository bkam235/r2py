"""LLM-based entity-to-Python-line mapping for verification scoring."""
from __future__ import annotations

import json
import os
import re

from . import llm as _llm

# Leading whitespace allowed: the model sometimes indents a copied sentinel to match a
# continuation line; _check_syntax already ignores indented ones, so the runner must too
# (an indented sentinel after a backslash continuation is a runtime SyntaxError).
_SENTINEL_RE = re.compile(r"^\s*# r2py:entity:\S+$")


_SENTINEL_ID_RE = re.compile(r"^\s*# r2py:entity:(\S+)$")


def ranges_from_sentinels(python_source: str) -> dict[str, list[tuple[int, int]]]:
    """Entity line ranges read off the ``# r2py:entity:<id>`` comments, deterministically.

    Same shape as ``map_entities_to_lines`` (1-based inclusive, an entity may own several ranges) and in
    the numbering of the source WITHOUT the sentinel lines, which is what verification runs.  A range
    starts on the line after its sentinel and ends on the last non-blank line before the next one.
    """
    clean: list[str] = []
    marks: list[tuple[str, int]] = []
    for line in python_source.splitlines():
        m = _SENTINEL_ID_RE.match(line)
        if m:
            marks.append((m.group(1), len(clean) + 1))
        else:
            clean.append(line)
    out: dict[str, list[tuple[int, int]]] = {}
    for i, (eid, start) in enumerate(marks):
        end = (marks[i + 1][1] - 1) if i + 1 < len(marks) else len(clean)
        while end >= start and not clean[end - 1].strip():
            end -= 1
        if end >= start:
            out.setdefault(eid, []).append((start, end))
    return out


class SentinelMappingError(RuntimeError):
    """Raised when the LLM fails to produce a valid entity-line mapping."""


def strip_sentinels(python_source: str) -> str:
    """Remove all ``# r2py:entity:<id>`` lines from Python source."""
    return "\n".join(
        line for line in python_source.splitlines()
        if not _SENTINEL_RE.match(line)
    )


def restore_sentinels(reference: str, candidate: str) -> str:
    """*candidate* with the entity sentinels of *reference* put back, by aligning unchanged lines.

    A rewrite that drops ``# r2py:entity:`` comments used to be attributed by a model (a sampled
    mapping: the aggregate of an unchanged source moved by up to 0.2).  Here every sentinel the
    candidate lost is re-inserted deterministically: before the first line of its entity body that
    survives unchanged, or, when the whole body was rewritten, right after the last surviving line that
    preceded it.  Sentinels the candidate kept stay where it put them.  The result is only as good as
    the alignment; ``ranges_from_sentinels`` on it tells the caller whether every entity got a range.
    """
    import difflib
    from collections import defaultdict

    def split(text):
        clean, marks = [], []
        for line in text.splitlines():
            m = _SENTINEL_ID_RE.match(line)
            if m:
                marks.append((m.group(1), len(clean)))
            else:
                clean.append(line)
        return clean, marks

    ref_clean, ref_marks = split(reference)
    cand_clean, cand_marks = split(candidate)
    sm = difflib.SequenceMatcher(a=[l.strip() for l in ref_clean], b=[l.strip() for l in cand_clean], autojunk=False)
    match: dict[int, int] = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            if ref_clean[blk.a + k].strip():
                match[blk.a + k] = blk.b + k

    # Lines the exact alignment missed: an assignment keeps its target name through a rewrite (the prompt requires it), so
    # an unmatched `name = ...` is paired with the unmatched `name = ...` in the same gap between two matched lines.
    assign = re.compile(r"^\s*([A-Za-z_][A-Za-z_0-9]*)\s*=[^=]")
    used = set(match.values())
    anchors = sorted(match)
    for i, line in enumerate(ref_clean):
        if i in match or not line.strip():
            continue
        m = assign.match(line)
        if not m:
            continue
        before = [a for a in anchors if a < i]
        after = [a for a in anchors if a > i]
        lo = match[before[-1]] + 1 if before else 0
        hi = match[after[0]] if after else len(cand_clean)
        for j in range(lo, hi):
            if j in used:
                continue
            mc = assign.match(cand_clean[j])
            if mc and mc.group(1) == m.group(1):
                match[i] = j
                used.add(j)
                anchors = sorted(match)
                break

    kept = defaultdict(list)                       # eid -> positions of its sentinels in the candidate
    for eid, pos in cand_marks:
        kept[eid].append(pos)
    seen = defaultdict(int)
    placed: list[tuple[int, int, str]] = []        # (candidate line index, order, eid)
    prev = 0
    for j, (eid, p0) in enumerate(ref_marks):
        n, seen[eid] = seen[eid], seen[eid] + 1
        if n < len(kept[eid]):
            target = kept[eid][n]
        else:
            end = ref_marks[j + 1][1] if j + 1 < len(ref_marks) else len(ref_clean)
            target = None
            for b in range(p0, end):
                if b in match:
                    target = max(match[b] - (b - p0), 0)   # same offset into the body as in the reference
                    target = min(target, match[b])
                    break
            if target is None:
                before = [match[b] for b in range(p0) if b in match]
                target = (max(before) + 1) if before else 0
        target = max(target, prev)                 # entities stay in the reference's order
        prev = target
        placed.append((target, j, eid))
    known = {e for e, _ in ref_marks}
    extra = [(pos, len(ref_marks) + k, eid) for k, (eid, pos) in enumerate(cand_marks) if eid not in known]
    placed = sorted(placed + extra)

    out: list[str] = []
    k = 0
    for i in range(len(cand_clean) + 1):
        while k < len(placed) and placed[k][0] == i:
            out.append(f"# r2py:entity:{placed[k][2]}")
            k += 1
        if i < len(cand_clean):
            out.append(cand_clean[i])
    return "\n".join(out)


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
    except json.JSONDecodeError:
        try:  # a lone backslash in a string ("Invalid \escape") is the usual culprit
            items = json.loads(re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', raw))
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

    # 2026-10-17: the mapping was sampled at the pinned temperature (1.0), so a candidate that lost its sentinels
    # (9% of agent candidates) got a different score on every verification, and the loop's accept decision was a
    # draw. Now: temperature 0, and the result is cached on disk per (model, entities, source), so the same source
    # always gets the same mapping, across harnesses, arms and runs.
    import hashlib
    import json as _json
    key = hashlib.sha1("|".join((model, entity_listing, clean)).encode("utf-8")).hexdigest()
    cache = _mapping_cache_dir() / f"{key}.json"
    if cache.exists():
        try:
            return {e: [tuple(r) for r in rs] for e, rs in _json.loads(cache.read_text(encoding="utf-8")).items()}
        except (ValueError, OSError):
            pass
    ranges = _map_uncached(messages, entity_ids, total_lines, model)
    try:
        cache.parent.mkdir(parents=True, exist_ok=True)
        tmp = cache.with_suffix(f".{os.getpid()}.tmp")
        tmp.write_text(_json.dumps(ranges), encoding="utf-8")
        tmp.replace(cache)
    except OSError:
        pass
    return ranges


def _mapping_cache_dir() -> "Path":
    from pathlib import Path
    env = os.environ.get("R2PY_MAPPING_CACHE")
    return Path(env) if env else Path(__file__).resolve().parents[2] / "work" / "mapping_cache"


def _map_uncached(messages, entity_ids, total_lines, model):
    raw = _llm.call(messages, system=_SYSTEM_PROMPT, model=model, max_tokens=8192, temperature=0.0)

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
            retry_messages, system=_SYSTEM_PROMPT, model=model, max_tokens=8192, temperature=0.0,
        )
        return _parse_response(raw2, entity_ids, total_lines)

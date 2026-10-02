"""Recombine seeds that failed in different places (Stage 11b).

Independent seeds crash at different statements and get different entities right.  Starting from the best
seed, an entity another seed translated better is spliced in (with the imports it needs), and the
verifier arbitrates: the change is kept only if the search objective improves.  No model call.
"""
from __future__ import annotations

import ast
import sys
from typing import TYPE_CHECKING

from ..stage2.stitch import rebuild_entity_line_map, splice_entity
from . import objective as _obj

if TYPE_CHECKING:
    from ..types import ScoreReport
    from .tools import HarnessTools

MARGIN = 0.05          # a donor entity must beat the base's by this much
MAX_VERIFIES = 8       # verifications spent per recombination


def _fragment(source: str, eid: str) -> str | None:
    """The body of a single-span entity in an annotated source, or None."""
    spans = rebuild_entity_line_map(source).get(eid)
    if not spans or len(spans) != 1:
        return None
    start, end = spans[0]
    return "\n".join(source.splitlines()[start:end])


def _import_nodes(source: str) -> list[ast.stmt]:
    try:
        return [n for n in ast.parse(source).body if isinstance(n, (ast.Import, ast.ImportFrom))]
    except SyntaxError:
        return []


def _with_donor_imports(base: str, donor: str) -> str:
    """*base* plus the top-level imports of *donor* that *base* lacks, placed after base's own imports."""
    have = {ast.dump(n) for n in _import_nodes(base)}
    missing = [ast.get_source_segment(donor, n) for n in _import_nodes(donor) if ast.dump(n) not in have]
    missing = [m for m in missing if m]
    if not missing:
        return base
    ends = [n.end_lineno for n in _import_nodes(base)]
    at = max(ends) if ends else 0
    lines = base.splitlines()
    return "\n".join(lines[:at] + missing + lines[at:]) + "\n"


def _donors(eid: str, base_score: float, pool: list[tuple[str, "ScoreReport"]]) -> list[tuple[float, str]]:
    """(entity score, fragment) from pool members that did this entity clearly better, best first."""
    out = []
    for src, rep in pool:
        es = rep.by_entity.get(eid)
        if es is None or not es.executed_ok:
            continue
        score = _obj.entity_score(es)
        frag = _fragment(src, eid)
        if frag and score > base_score + MARGIN:
            out.append((score, frag, src))
    out.sort(key=lambda x: -x[0])
    return [(s, f, src) for s, f, src in out]


def recombine(pool: list[tuple[str, "ScoreReport"]], harness: "HarnessTools",
              max_verifies: int = MAX_VERIFIES) -> tuple[str, "ScoreReport"] | None:
    """Best of *pool* improved by donor entities; None if nothing beat the best member.

    *pool* holds (annotated source, report) per seed.  Entities are tried crashed ones first, then by
    ascending score; each is replaced by the best donor's version, and kept if the search objective improves.
    """
    from .agent import _check_syntax
    from ..stage0.env.module_check import unavailable_imports
    from ..stage0.sandbox.py_sandbox import _SKIP_PACKAGES

    if len(pool) < 2:
        return None
    base_src, base_rep = pool[0]
    for src, rep in pool[1:]:
        if _obj.better(rep, base_rep):
            base_src, base_rep = src, rep
    start_rep = base_rep
    if hasattr(harness, "note_reference"):
        harness.note_reference(base_src)

    crashed = list(getattr(base_rep, "crash_entities", []) or [])
    order = crashed + sorted((e for e in base_rep.by_entity if e not in crashed),
                             key=lambda e: _obj.entity_score(base_rep.by_entity[e]))
    spent = 0
    for eid in order:
        if spent >= max_verifies:
            break
        es = base_rep.by_entity.get(eid)
        donors = _donors(eid, _obj.entity_score(es) if es is not None else 0.0, pool)
        if not donors or base_src.count(f"# r2py:entity:{eid}\n") != 1:
            continue
        _score, frag, donor_src = donors[0]
        new_src, _err = splice_entity(base_src, eid, frag)
        if new_src is None:
            continue
        new_src = _with_donor_imports(new_src, donor_src)
        if _check_syntax(new_src) or unavailable_imports(new_src, _SKIP_PACKAGES):
            continue
        spent += 1
        try:
            rep = harness.verify(new_src)
        except Exception as exc:
            print(f"[Recombine] verification failed: {exc}", file=sys.stderr)
            continue
        if _obj.better(rep, base_rep):
            print(f"[Recombine] entity {eid}: {base_rep.aggregate:.3f} -> {rep.aggregate:.3f}", file=sys.stderr)
            base_src = getattr(harness, "last_annotated_source", None) or new_src
            base_rep = rep
    if _obj.better(base_rep, start_rep):
        return base_src, base_rep
    return None

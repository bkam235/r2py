"""Pattern retrieval: package-first, AST-shape second, token-similarity last (§6.4)."""
from __future__ import annotations

import hashlib
from itertools import groupby
from typing import TYPE_CHECKING

from .pattern import Pattern
from ..types import PatternId

if TYPE_CHECKING:
    from .store import PatternStore
    from .index import PatternIndex


def retrieve(
    entity: object,
    k: int,
    store: "PatternStore",
    index: "PatternIndex",
    no_seeds: bool = False,
) -> list[Pattern]:
    """Return at most k patterns relevant to entity.

    Ranking (§6.4):
    1. Filter to patterns matching entity.package (or all packages if entity has none).
    2. Within that set, rank by AST-shape similarity (token overlap of entity kind).
    3. Tie-break by raw token similarity of guidance text vs entity name.
    Excludes contradicted patterns and (when no_seeds=True) seed patterns.
    """
    package = getattr(entity, "package", None) or ""
    entity_name = getattr(entity, "name", "") or ""
    entity_kind = _entity_kind_str(entity)

    # Step 1: gather candidate IDs by package.
    # When the entity's package has no dedicated patterns (common for R-only
    # packages like withr where Python patterns live under package=""), fall
    # back to the full empty-package bucket so general-purpose patterns are
    # still retrieved.
    if package:
        candidate_ids = index.lookup(package)
        if not candidate_ids:
            candidate_ids = index.all_ids()
    else:
        candidate_ids = index.all_ids()

    if not candidate_ids:
        return []

    # Step 2: load and filter
    candidates: list[Pattern] = []
    for pid in candidate_ids:
        pat = store.get(pid)
        if pat is None:
            continue
        if pat.confidence == "contradicted":
            continue
        if no_seeds and pat.seed:
            continue
        # Tentative patterns need at least 2 genuine improvements (score > 0)
        # before they are shown to Stage 2/3. Tie interactions (tracked in
        # tie_count) do not count — they carry no positive signal. Seeds are
        # always kept regardless of evidence count.
        if pat.confidence == "tentative" and not pat.seed:
            real_evidence = sum(1 for e in pat.evidence if e.score > 0.0)
            if real_evidence < 2:
                continue
        candidates.append(pat)

    if not candidates:
        return []

    # Step 3: rank
    def score(pat: Pattern) -> tuple[int, float]:
        # Tier 1: exact package match (0) vs wildcard fallback (1)
        pkg_tier = 0 if pat.package == package else 1
        # Tier 2: AST-shape token overlap (negated for descending sort)
        shape_sim = -_token_overlap(entity_kind, pat.id)
        return (pkg_tier, shape_sim)

    candidates.sort(key=score)

    # Tie-break by guidance token similarity to entity name
    # (stable sort preserves prior ordering within tied groups)
    def tiebreak(pat: Pattern) -> float:
        return -_token_overlap(entity_name, pat.guidance)

    # Group by (pkg_tier, shape_sim) and within each group sort by tiebreak
    result: list[Pattern] = []
    for _, group in groupby(candidates, key=score):
        group_list = sorted(group, key=tiebreak)
        result.extend(group_list)

    return result[:k]


def entity_ast_shape_hash(entity: object) -> str:
    """Compute a coarse AST shape hash for an entity.

    Uses entity kind value as the shape signal — sufficient for retrieval
    without needing the full AST tree at query time.
    """
    kind_str = _entity_kind_str(entity)
    if not kind_str:
        return ""
    return hashlib.md5(kind_str.encode()).hexdigest()[:8]


def _entity_kind_str(entity: object) -> str:
    kind = getattr(entity, "kind", None)
    if kind is None:
        return ""
    return getattr(kind, "value", str(kind))


def _token_overlap(a: str, b: str) -> float:
    """Jaccard token overlap between two strings.

    Splits on whitespace AND on `_`, `.`, `-` so that snake_case identifiers
    and dotted pattern IDs are tokenised into sub-words.  This lets the
    retriever rank e.g. `withr.with_locale` high for an entity named
    `with_locale` even when there are no exact-string matches.
    """
    if not a or not b:
        return 0.0
    import re as _re
    _split = lambda s: set(_re.split(r"[\s._\-]+", s.lower())) - {""}
    toks_a = _split(a)
    toks_b = _split(b)
    if not toks_a or not toks_b:
        return 0.0
    return len(toks_a & toks_b) / len(toks_a | toks_b)

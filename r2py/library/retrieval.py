"""Pattern retrieval: the pattern for exactly this (package, function), or nothing (§6.4)."""
from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

from .pattern import EditExample, Pattern, correction_functions, pattern_id, pattern_key

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
    """Return the pattern for this entity's (package, function), if the library has one.

    Patterns are keyed by ``pattern_id(package, function)`` and an entity's key is given by
    ``pattern_key``, so this is a direct lookup. There is deliberately no fallback: a pattern
    for some other function is noise in the prompt, not guidance. Excludes contradicted
    patterns and (when no_seeds=True) seed patterns. ``k`` and ``index`` are unused (at most
    one pattern can match); they stay so the facade and the callers keep one signature.
    """
    key = pattern_key(entity)
    if key is None:
        return []
    pat = store.get(pattern_id(*key))
    return [pat] if pat is not None and _usable(pat, no_seeds) else []


def _usable(pat: Pattern, no_seeds: bool) -> bool:
    """Whether a pattern may be shown to the translator."""
    if pat.confidence == "contradicted":
        return False
    if no_seeds and pat.seed:
        return False
    # Tentative patterns need at least 2 genuine improvements (score > 0) before they
    # are shown to Stage 2/3. Tie interactions (tracked in tie_count) do not count —
    # they carry no positive signal. Seeds are always kept regardless of evidence count.
    if pat.confidence == "tentative" and not pat.seed:
        return sum(1 for e in pat.evidence if e.score > 0.0) >= 2
    return True


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


def retrieve_corrections(
    base_r_calls: list[str],
    store: "PatternStore",
    k: int = 1,
    no_seeds: bool = False,
) -> list[EditExample]:
    """Verified wrong-then-corrected pairs for the base-R functions an entity calls.

    Each correction is stored on the pattern of every base-R function it involves, so the
    functions an entity calls are the (cross-package) key. Ranked by how many of the entity's
    functions the correction involves, then by its score gain; a correction found under
    several functions is returned once.
    """
    keys = set(correction_functions(base_r_calls))
    found: dict[tuple, EditExample] = {}
    for qualified in sorted(keys):
        package, fn = qualified.split("::")
        pat = store.get(pattern_id(package, fn))
        if pat is None or not _usable(pat, no_seeds):
            continue
        for ex in pat.edit_examples:
            found[(ex.script_id, ex.r_snippet, ex.new_code)] = ex
    ranked = sorted(found.values(), key=lambda ex: (
        -len(keys & set(ex.functions)), -ex.score_delta, ex.script_id, ex.r_snippet))
    return ranked[:k]


def retrieve_base_patterns(
    entity: object,
    store: "PatternStore",
    no_seeds: bool = False,
) -> list[Pattern]:
    """Patterns for the base-R functions called anywhere inside an entity.

    Base R is shared by every package, so each such pattern holds verified statements from any
    script that used the function; its first example is the most focused one. The function
    that keys the entity itself is left to ``retrieve``.
    """
    key = pattern_key(entity)
    own_id = pattern_id(*key) if key else None
    found: list[Pattern] = []
    for qualified in correction_functions(getattr(entity, "base_r_calls", None) or []):
        pid = pattern_id(*qualified.split("::"))
        pat = store.get(pid) if pid != own_id else None
        if pat is not None and pat.translation_examples and _usable(pat, no_seeds):
            found.append(pat)
    return found

"""Sole mutator of the Pattern Library (§6.3, §7.7).

Only this module calls store.save() and index.rebuild(). All other code
routes through record_evidence / record_tie / record_contradiction.
"""
from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from .pattern import (
    EditExample, EvidenceEntry, Pattern, TranslationExample, r_snippet_hash,
)
from ..types import Edit

if TYPE_CHECKING:
    from .store import PatternStore
    from .index import PatternIndex
    from ..types import PatternId


def record_evidence(
    edit: Edit,
    score_delta: float,
    script_id: str,
    entity_id: str,
    verification_path: str,
    store: "PatternStore",
    index: "PatternIndex",
    ast_shape_hash: str = "",
    entity_package: str = "",
    # Entity-level example recording (plan: entity-level examples).
    r_snippet: str = "",
    py_snippet: str = "",
    failure_class: str = "",
    old_code: str = "",
    new_code: str = "",
) -> None:
    """Append a verified evidence entry to the attributed pattern (§7.7).

    New patterns are created only here (on strict improvement), never on ties
    or contradictions — that is what keeps the library from bloating.

    When r_snippet + py_snippet are provided and score_delta > 0, a
    TranslationExample is appended (capped at 3 per pattern, highest score wins).
    When failure_class + old_code + new_code are provided and score_delta > 0,
    an EditExample is appended (capped at 5 per failure_class, highest delta wins).
    """
    if not edit.pattern_id:
        return
    pat = _get_or_create(edit.pattern_id, edit, store, entity_package=entity_package)
    if pat is None:
        # New pattern proposed without guidance — skip rather than create garbage.
        return
    entry = EvidenceEntry(
        script_id=script_id,
        score=max(0.0, score_delta),
        verification_path=verification_path,
        variable=entity_id,
    )
    pat.evidence.append(entry)

    if score_delta > 0:
        if r_snippet and py_snippet:
            _add_translation_example(pat, TranslationExample(
                r_hash=r_snippet_hash(r_snippet),
                r_snippet=r_snippet[:300],
                py_snippet=py_snippet[:600],
                score=max(0.0, score_delta),
                script_id=script_id,
            ))
        if failure_class and old_code and new_code:
            _add_edit_example(pat, EditExample(
                failure_class=failure_class,
                old_code=old_code[:300],
                new_code=new_code[:300],
                score_delta=score_delta,
                script_id=script_id,
            ))

    pat.last_review = date.today().isoformat()
    store.save(pat)
    _upsert_index(pat, index, ast_shape_hash=ast_shape_hash)
    # Evidence raises the demotion threshold (ceil(|evidence|/2)), so it can
    # never trigger a demotion by itself.  Epistemology is only run after
    # contradictions, where it may actually fire.


def record_tie(
    edit: Edit,
    script_id: str,
    entity_id: str,
    store: "PatternStore",
    index: "PatternIndex",
) -> None:
    """Record a tie on an EXISTING pattern only (§7.7).

    Ties are counted separately from improvement evidence so they do not
    inflate the demotion threshold. Ties do NOT create new patterns.
    """
    if not edit.pattern_id:
        return
    pat = store.get(edit.pattern_id)
    if pat is None:
        return
    pat.tie_count += 1
    pat.last_review = date.today().isoformat()
    store.save(pat)
    _upsert_index(pat, index)


def record_contradiction(
    edit: Edit,
    observed: float,
    script_id: str,
    entity_id: str,
    store: "PatternStore",
    index: "PatternIndex",
) -> None:
    """Append a contradiction to an EXISTING pattern only (§7.7).

    Contradictions do NOT create new patterns. An unrecognised slug means the
    edit was never accepted, so there is no established rule to contradict.
    """
    if not edit.pattern_id:
        return
    pat = store.get(edit.pattern_id)
    if pat is None:
        return
    pat.contradictions.append(
        f"{script_id}/{entity_id}: score regressed to {observed:.3f}"
    )
    pat.last_review = date.today().isoformat()
    store.save(pat)
    _upsert_index(pat, index, contradicted_at_run=index.total_runs())
    _run_epistemology(store, index)


# ------------------------------------------------------------------ #
# Helpers                                                              #
# ------------------------------------------------------------------ #

def _get_or_create(
    pattern_id: PatternId,
    edit: Edit,
    store: "PatternStore",
    entity_package: str = "",
) -> "Pattern | None":
    pat = store.get(pattern_id)
    if pat is not None:
        # Backfill package if the pattern was previously created without one.
        if not pat.package and entity_package:
            pat.package = entity_package
        return pat
    # New pattern proposed by Stage 3; starts tentative (§6.3).
    # Only called from record_evidence (strict-improvement path) — not from
    # record_tie or record_contradiction, which skip unknown patterns.
    # Require non-empty guidance: a pattern with no rule description has no
    # value in the library and would only confuse Stage 2/3.
    guidance = edit.guidance.strip() if edit.guidance else ""
    if not guidance:
        return None
    package = entity_package or _infer_package(edit)
    return Pattern(
        id=pattern_id,
        package=package,
        confidence="tentative",
        seed=False,
        guidance=guidance,
        created=date.today().isoformat(),
        last_review=date.today().isoformat(),
    )


def _infer_package(edit: Edit) -> str:
    return str(edit.params.get("package", ""))


def _upsert_index(pat: Pattern, index: "PatternIndex", ast_shape_hash: str = "",
                  contradicted_at_run: int | None = None) -> None:
    index.upsert_meta(
        pattern_id=pat.id,
        package=pat.package,
        confidence=pat.confidence,
        evidence_count=len(pat.evidence),
        contradictions_count=len(pat.contradictions),
        seed=pat.seed,
        ast_shape_hash=ast_shape_hash,
        contradicted_at_run=contradicted_at_run,
    )


def _run_epistemology(store: "PatternStore", index: "PatternIndex") -> None:
    from . import epistemology
    epistemology.review(store, index)


def _add_translation_example(pat: Pattern, ex: "TranslationExample") -> None:
    """Add a TranslationExample to pat, deduplicating by r_hash and capping at 3."""
    for i, e in enumerate(pat.translation_examples):
        if e.r_hash == ex.r_hash:
            if ex.score > e.score:
                pat.translation_examples[i] = ex
            return
    pat.translation_examples.append(ex)
    pat.translation_examples.sort(key=lambda e: -e.score)
    pat.translation_examples = pat.translation_examples[:3]



def _add_edit_example(pat: Pattern, ex: "EditExample") -> None:
    """Add an EditExample to pat, capping at 5 per failure_class (highest delta kept)."""
    same = [e for e in pat.edit_examples if e.failure_class == ex.failure_class]
    other = [e for e in pat.edit_examples if e.failure_class != ex.failure_class]
    same.append(ex)
    same.sort(key=lambda e: -e.score_delta)
    pat.edit_examples = other + same[:5]

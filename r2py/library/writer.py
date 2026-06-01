"""Sole mutator of the Pattern Library (§6.3, §7.7).

Only this module calls store.save() and index.rebuild(). All other code
routes through record_evidence / record_tie / record_contradiction.
"""
from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from .pattern import EvidenceEntry, Pattern
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
) -> None:
    """Append a verified evidence entry to the attributed pattern (§7.7).

    New patterns are created only here (on strict improvement), never on ties
    or contradictions — that is what keeps the library from bloating.
    """
    if not edit.pattern_id:
        return
    pat = _get_or_create(edit.pattern_id, edit, store, entity_package=entity_package)
    entry = EvidenceEntry(
        script_id=script_id,
        score=max(0.0, score_delta),
        verification_path=verification_path,
        variable=entity_id,
    )
    pat.evidence.append(entry)
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

    Ties do NOT create new patterns. If the pattern doesn't exist yet it was
    never accepted, so there is no established rule to record the tie against.
    """
    if not edit.pattern_id:
        return
    pat = store.get(edit.pattern_id)
    if pat is None:
        return
    entry = EvidenceEntry(
        script_id=script_id,
        score=0.0,
        verification_path="tie",
        variable=entity_id,
    )
    pat.evidence.append(entry)
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
) -> Pattern:
    pat = store.get(pattern_id)
    if pat is not None:
        # Backfill package if the pattern was previously created without one.
        if not pat.package and entity_package:
            pat.package = entity_package
        return pat
    # New pattern proposed by Stage 3; starts tentative (§6.3).
    # Only called from record_evidence (strict-improvement path) — not from
    # record_tie or record_contradiction, which skip unknown patterns.
    package = entity_package or _infer_package(edit)
    return Pattern(
        id=pattern_id,
        package=package,
        confidence="tentative",
        seed=False,
        guidance=f"Auto-created from edit {edit.kind.value} (no guidance yet).",
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

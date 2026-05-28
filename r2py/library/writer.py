"""Sole mutator of the Pattern Library (§6.3, §7.7).

Only this module calls store.save() and index.rebuild(). All other code
routes through record_evidence / record_tie / record_contradiction.
"""
from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from .pattern import EvidenceEntry, Pattern
from ..types import Edit, PatternId

if TYPE_CHECKING:
    from .store import PatternStore
    from .index import PatternIndex


def record_evidence(
    edit: Edit,
    score_delta: float,
    script_id: str,
    entity_id: str,
    verification_path: str,
    store: "PatternStore",
    index: "PatternIndex",
) -> None:
    """Append a verified evidence entry to the attributed pattern (§7.7)."""
    if not edit.pattern_id:
        return
    pat = _get_or_create(edit.pattern_id, edit, store)
    entry = EvidenceEntry(
        script_id=script_id,
        score=max(0.0, score_delta),
        verification_path=verification_path,
        variable=entity_id,
    )
    pat.evidence.append(entry)
    pat.last_review = date.today().isoformat()
    store.save(pat)
    _upsert_index(pat, index)
    _run_epistemology(store, index)


def record_tie(
    edit: Edit,
    script_id: str,
    entity_id: str,
    store: "PatternStore",
    index: "PatternIndex",
) -> None:
    """Record a tie (score unchanged); weak evidence, not accepted into beam (§7.7)."""
    if not edit.pattern_id:
        return
    pat = _get_or_create(edit.pattern_id, edit, store)
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
    """Append a contradiction and trigger epistemology review (§7.7)."""
    if not edit.pattern_id:
        return
    pat = _get_or_create(edit.pattern_id, edit, store)
    pat.contradictions.append(
        f"{script_id}/{entity_id}: score regressed to {observed:.3f}"
    )
    pat.last_review = date.today().isoformat()
    store.save(pat)
    _upsert_index(pat, index)
    _run_epistemology(store, index)


# ------------------------------------------------------------------ #
# Helpers                                                              #
# ------------------------------------------------------------------ #

def _get_or_create(pattern_id: PatternId, edit: Edit, store: "PatternStore") -> Pattern:
    pat = store.get(pattern_id)
    if pat is not None:
        return pat
    # New pattern proposed by Stage 3; starts tentative (§6.3)
    return Pattern(
        id=pattern_id,
        package=_infer_package(edit),
        confidence="tentative",
        seed=False,
        guidance=f"Auto-created from edit {edit.kind.value} (no guidance yet).",
        created=date.today().isoformat(),
        last_review=date.today().isoformat(),
    )


def _infer_package(edit: Edit) -> str:
    return str(edit.params.get("package", ""))


def _upsert_index(pat: Pattern, index: "PatternIndex") -> None:
    index.upsert_meta(
        pattern_id=pat.id,
        package=pat.package,
        confidence=pat.confidence,
        evidence_count=len(pat.evidence),
        contradictions_count=len(pat.contradictions),
        seed=pat.seed,
    )


def _run_epistemology(store: "PatternStore", index: "PatternIndex") -> None:
    from . import epistemology
    epistemology.review(store, index)

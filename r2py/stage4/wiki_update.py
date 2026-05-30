"""Pattern Library mutation after verification outcomes (§7.7).

This is the ONLY module in the system that calls library.writer.* mutators.
Every change to the library has a named cause (the Edit's pattern_id) and is
validated by the score change before being persisted.
"""
from __future__ import annotations

import hashlib

from ..types import Edit


def _script_id(r_source: str) -> str:
    """Derive a stable script id from R source text."""
    return hashlib.sha1(r_source.encode()).hexdigest()[:12]


def after_accepted_edit(
    edit: Edit,
    new_score: float,
    library,
    r_source: str = "",
) -> None:
    """Record evidence after a strictly-improving edit (new_score > parent_score)."""
    if edit.pattern_id is None:
        return
    sid = _script_id(r_source) if r_source else "unknown"
    library.record_evidence(edit, score_delta=new_score, script_id=sid, verification_path="exact")


def after_tie(
    edit: Edit,
    score: float,
    library,
    r_source: str = "",
) -> None:
    """Record weak evidence after a tie (new_score == parent_score).

    The candidate is NOT accepted into the beam (§4.1), only weak evidence logged.
    """
    if edit.pattern_id is None:
        return
    sid = _script_id(r_source) if r_source else "unknown"
    library.record_tie(edit, script_id=sid)


def after_rejected_edit(
    edit: Edit,
    library,
    r_source: str = "",
) -> None:
    """Record a contradiction after a regressing edit."""
    if edit.pattern_id is None:
        return
    sid = _script_id(r_source) if r_source else "unknown"
    library.record_contradiction(edit, observed=0.0, script_id=sid)


def maybe_review(
    n_translations: int,
    library,
    every_n: int = 10,
) -> list[str]:
    """Run epistemology review every every_n translations."""
    if n_translations > 0 and n_translations % every_n == 0:
        return library.epistemology_review()
    return []

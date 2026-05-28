"""Stage 3 — Editor: typed edits to improve translation score (§8)."""
from __future__ import annotations

from ..types import Candidate, Edit


def propose_edit(candidate: Candidate, library: object) -> Edit:
    """Propose a typed edit for the weakest entity in the candidate."""
    raise NotImplementedError("Stage 3 not yet implemented (architecture step 6)")


def apply_edit(translation: str, edit: Edit) -> str:
    """Apply a typed edit to a Python source string, returning the modified source."""
    raise NotImplementedError("Stage 3 not yet implemented (architecture step 6)")

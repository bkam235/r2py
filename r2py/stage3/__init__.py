"""Stage 3 — Editor: typed edits to improve translation score (§8)."""
from __future__ import annotations

from ..types import Candidate, Edit
from .edit_types import apply_edit
from .history import EditHistory


def propose_edit(
    candidate: Candidate,
    library: object,
    script_map: object = None,
    history: EditHistory | None = None,
    iteration: int = 0,
    model: str | None = None,
    _collector: object = None,
) -> Edit:
    """Propose a typed edit for the weakest entity in the candidate.

    script_map and history are optional for backward compatibility with the §4.1
    pseudocode signature (candidate, library); the loop (step 7) will pass them.
    """
    from .editor import propose_edit as _propose
    from ..stage2.llm import _DEFAULT_MODEL
    return _propose(
        candidate,
        library,
        script_map,
        history if history is not None else EditHistory(),
        iteration,
        model=model if model is not None else _DEFAULT_MODEL,
        _collector=_collector,
    )


def apply_edit(translation: str, edit: Edit) -> str:
    """Apply a typed edit to a Python source string, returning the modified source."""
    from .edit_types import apply_edit as _apply
    return _apply(translation, edit)

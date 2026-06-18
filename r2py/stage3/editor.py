"""Stage 3 editor entry point (§8.1).

propose_edit() manages the epsilon schedule and delegates to policy.propose().
apply_edit() is re-exported from edit_types for use by the loop.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..stage2 import llm as _llm
from . import policy as _policy
from .edit_types import apply_edit  # noqa: F401 — re-exported for callers
from .history import EditHistory

if TYPE_CHECKING:
    from ..library import PatternLibrary
    from ..stage1.script_map import ScriptMap
    from ..types import Candidate, Edit


def propose_edit(
    candidate: "Candidate",
    library: "PatternLibrary",
    script_map: "ScriptMap",
    history: "EditHistory",
    iteration: int = 0,
    model: str = _llm._DEFAULT_MODEL,
    meta_model: str = _llm._DEFAULT_MODEL,
    _collector: object = None,
) -> "Edit":
    """Propose a typed edit to improve the candidate's score.

    epsilon decays from 0.30 (iter 0) to 0.05 (iter ≥ 10), favouring
    exploitation as the loop matures.
    """
    epsilon = _epsilon(iteration)
    return _policy.propose(candidate, script_map, library, history, epsilon, model,
                           meta_model=meta_model, _collector=_collector)


def _epsilon(iteration: int) -> float:
    return max(0.05, 0.30 - iteration * 0.025)

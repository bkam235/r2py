"""ε-greedy edit proposal policy for Stage 3 (§8.4).

EXPLOIT: follow the best retrieved Pattern's guidance.
EXPLORE: propose freely, guided only by the verifier's feedback.
"""
from __future__ import annotations

import random
from typing import TYPE_CHECKING

from ..stage2 import llm as _llm
from ..types import Edit, EntityScore
from . import prompt as _prompt
from .attributor import attribute, AttributionError
from .edit_types import dict_to_edit

if TYPE_CHECKING:
    from ..library import PatternLibrary
    from ..stage1.script_map import ScriptMap
    from ..types import Candidate
    from .history import EditHistory


def propose(
    candidate: "Candidate",
    script_map: "ScriptMap",
    library: "PatternLibrary",
    history: "EditHistory",
    epsilon: float = 0.2,
    model: str = _llm._DEFAULT_MODEL,
) -> Edit:
    """Propose a typed edit targeting the weakest entity in the candidate.

    Tries each entity in ascending score order, skipping already-tried edits.
    Raises RuntimeError if all entities are exhausted or the LLM fails.
    """
    if script_map is None or not getattr(script_map, "entities", {}):
        raise RuntimeError(
            "propose() requires a ScriptMap with populated entities; "
            "pass script_map to stage3.propose_edit() (§4.1 loop)"
        )

    ordered = _weak_first(candidate)
    if not ordered:
        raise RuntimeError("no entities to edit: ScoreReport.by_entity is empty")

    for eid in ordered:
        entity = _get_entity(script_map, eid)
        if entity is None:
            continue

        entity_score = candidate.decomp.by_entity.get(eid, EntityScore(entity_id=eid))
        feedback = [f for f in candidate.decomp.feedback if f.entity_id == eid]

        patterns = library.retrieve(entity, k=3) if hasattr(library, "retrieve") else []
        exploit = bool(patterns) and random.random() > epsilon

        messages = _prompt.build_edit_prompt(
            entity=entity,
            entity_score=entity_score,
            feedback=feedback,
            translation=candidate.translation,
            patterns=patterns if exploit else [],
            history=history,
            exploit=exploit,
        )

        raw = _llm.call(messages, _prompt.STAGE3_SYSTEM_PROMPT, model=model)

        d = _prompt.parse_edit_response(raw)
        if d is None:
            continue

        try:
            edit = dict_to_edit(d)
        except (ValueError, KeyError):
            continue

        # Use pattern_id from the LLM response; in exploit mode also accept the retrieved id.
        pid = d.get("pattern_id") or (patterns[0].id if exploit and patterns else None)
        try:
            attributed = attribute(edit, pid)
        except AttributionError:
            continue

        if history.was_tried(attributed):
            continue

        return attributed

    raise RuntimeError("no untried edits could be proposed for any entity")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _weak_first(candidate: "Candidate") -> list[str]:
    """Return entity IDs sorted by ascending average score."""
    scores = candidate.decomp.by_entity
    return sorted(scores.keys(), key=lambda eid: _avg_score(scores[eid]))


def _avg_score(es: EntityScore) -> float:
    vals = [
        es.type_match,
        es.control_flow_match,
        es.data_output,
        es.variable_output,
        es.callable_output,
        es.side_effects,
    ]
    return sum(vals) / len(vals)


def _get_entity(script_map: "ScriptMap", eid: str) -> object | None:
    """Return the Entity for eid, or None if script_map has no entities dict."""
    entities = getattr(script_map, "entities", {})
    return entities.get(eid)

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
    _collector: object = None,
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

    from ..library.bandit import BanditModel as _BanditModel
    from ..library import bandit as _bandit
    from ..types import EditKind
    bandit_model = getattr(library, "_bandit_model", None)

    for eid in ordered:
        entity = _get_entity(script_map, eid)
        if entity is None:
            continue

        entity_score = candidate.decomp.by_entity.get(eid, EntityScore(entity_id=eid))
        feedback = [f for f in candidate.decomp.feedback if f.entity_id == eid]

        patterns = library.retrieve(entity, k=3) if hasattr(library, "retrieve") else []
        exploit = bool(patterns) and random.random() > epsilon

        # D6: if a trained bandit model is available, use it to choose the preferred
        # edit kind and pass that hint to the prompt (bandit handles exploration itself).
        bandit_hint: str | None = None
        if isinstance(bandit_model, _BanditModel):
            context = _bandit.extract_context(
                entity_score,
                getattr(getattr(entity, "kind", None), "value", ""),
                getattr(entity, "package", None) or "",
            )
            all_arms = [e.value for e in EditKind]
            bandit_hint = _bandit.choose_action(bandit_model, context, all_arms)

        messages = _prompt.build_edit_prompt(
            entity=entity,
            entity_score=entity_score,
            feedback=feedback,
            translation=candidate.translation,
            patterns=patterns if exploit else [],
            history=history,
            exploit=exploit,
            preferred_edit_kind=bandit_hint,
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

        if _collector is not None and patterns:
            _collector.episodes.append(_make_episode(entity, patterns, pid, exploit))

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
    # Use only execution-outcome fields for edit priority. type_match, control_flow_match,
    # and callable_output include kind-specific 1.0 constants for non-callable entities
    # (e.g. LIBRARY_IMPORT always gets callable_output=1.0) which would inflate the
    # apparent score of a failed entity and deprioritize it from editing.
    vals = [es.data_output, es.variable_output, es.side_effects]
    return sum(vals) / len(vals)


def _get_entity(script_map: "ScriptMap", eid: str) -> object | None:
    """Return the Entity for eid, or None if script_map has no entities dict."""
    entities = getattr(script_map, "entities", {})
    return entities.get(eid)


def _make_episode(entity: object, patterns: list, chosen_id: "str | None", exploit: bool) -> object:
    """Build a RetrievalEpisode (outcome/score_delta stamped later by the loop)."""
    from ..types import RetrievalEpisode, RetrievalEpisodeCandidate
    from ..library.retrieval import _token_overlap, _entity_kind_str

    package = getattr(entity, "package", None) or ""
    entity_name = getattr(entity, "name", "") or ""
    entity_kind = _entity_kind_str(entity)

    candidates = []
    for rank, pat in enumerate(patterns):
        pkg_match = pat.package == package
        ast_sim = _token_overlap(entity_kind, pat.id)
        tok_sim = _token_overlap(entity_name, pat.guidance)
        candidates.append(RetrievalEpisodeCandidate(
            pattern_id=pat.id,
            rank=rank,
            package_match=pkg_match,
            ast_shape_sim=ast_sim,
            token_sim=tok_sim,
            confidence=pat.confidence,
            evidence_count=len(pat.evidence),
            contradiction_count=len(pat.contradictions),
            last_review=pat.last_review or "",
        ))

    return RetrievalEpisode(
        query_entity_id=getattr(entity, "id", ""),
        query_entity_kind=entity_kind,
        query_package=package,
        query_entity_name=entity_name,
        candidates=candidates,
        chosen_pattern_id=chosen_id,
        exploit_mode=exploit,
        outcome=None,
        score_delta=None,
        script_id="",
        iteration=0,
    )

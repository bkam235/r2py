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

    ordered = _weak_first(candidate, script_map)
    if not ordered:
        raise RuntimeError("no entities to edit: ScoreReport.by_entity is empty")

    from ..library.bandit import BanditModel as _BanditModel
    from ..library import bandit as _bandit
    from ..types import EditKind
    bandit_model = getattr(library, "_bandit_model", None)

    # Max edits tried for any single entity before moving on (prevents cycling when
    # the LLM generates slight param variations that all produce the same bad score).
    _MAX_ATTEMPTS_PER_ENTITY = 3

    for eid in ordered:
        if history.count_for_entity(eid) >= _MAX_ATTEMPTS_PER_ENTITY:
            continue

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
            r_source=_entity_r_source(entity, script_map),
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

        # Redirect edits that target a completely different entity than the one
        # we asked the LLM to fix. Redirect rather than reject so the edit
        # still gets applied — the LLM's mechanical params are usually correct,
        # only the entity_ids field is wrong.
        if attributed.entity_ids and eid not in attributed.entity_ids:
            attributed = Edit(
                kind=attributed.kind,
                entity_ids=[eid],
                params=attributed.params,
                pattern_id=attributed.pattern_id,
            )

        return attributed

    raise RuntimeError("no untried edits could be proposed for any entity")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _weak_first(candidate: "Candidate", script_map: object = None) -> list[str]:
    """Return entity IDs sorted by ascending average score.

    Tie-break order:
    1. Entities with specific feedback in the current ScoreReport (more actionable).
    2. FUNCTION_CALL / EXTERNAL_SYMBOL entities before LIBRARY_IMPORT / VARIABLE /
       CONSTANT — callables are more likely to be execution failures.
    """
    from ..types import EntityKind
    scores = candidate.decomp.by_entity
    entities = getattr(script_map, "entities", {}) if script_map is not None else {}
    feedback_eids = {f.entity_id for f in candidate.decomp.feedback}

    def _sort_key(eid: str) -> tuple:
        es = scores[eid]
        avg = _avg_score(es)
        has_feedback = 0 if eid in feedback_eids else 1
        entity = entities.get(eid)
        kind_val = getattr(entity, "kind", None) if entity else None
        is_callable = kind_val in (EntityKind.FUNCTION_CALL, EntityKind.EXTERNAL_SYMBOL,
                                   EntityKind.FUNCTION_DEF)
        priority = 0 if is_callable else 1
        return (avg, has_feedback, priority)

    return sorted(scores.keys(), key=_sort_key)


def _avg_score(es: EntityScore) -> float:
    # Use only execution-outcome fields for edit priority. type_match, control_flow_match,
    # and callable_output include kind-specific 1.0 constants for non-callable entities
    # (e.g. LIBRARY_IMPORT always gets callable_output=1.0) which would inflate the
    # apparent score of a failed entity and deprioritize it from editing.
    vals = [es.data_output, es.variable_output, es.side_effects]
    base = sum(vals) / len(vals)
    # Penalise entities that did not execute (crash or post-crash): they are more
    # likely to be causing the failure and should rank ahead of pre-crash entities
    # that already ran successfully (crash attribution via §7.4 decompose).
    return base if es.executed_ok else max(0.0, base - 0.1)


def _entity_r_source(entity: object, script_map: object) -> str:
    """Extract the R source lines for an entity from the ScriptMap."""
    source = getattr(script_map, "source", "") or ""
    if not source:
        return ""
    span = getattr(entity, "source_span", None)
    if span is None:
        return ""
    lines = source.splitlines()
    start = getattr(span, "start_line", 0)
    end = getattr(span, "end_line", start)
    return "\n".join(lines[start:end + 1])


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

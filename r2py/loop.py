"""Beam/strict-improvement translation loop (§4.1).

W=1 reduces to strict hill-climbing. W>1 holds a population of candidates and
accepts only strict improvements, preventing neutral drift and cycling.
"""
from __future__ import annotations

import ast as _ast_mod
import dataclasses
import hashlib
import json
from pathlib import Path
from typing import TYPE_CHECKING

from .types import (
    Candidate, EpisodeCollector, EffectBundle, PolicyTransition, Proposal, TranslateResult,
)
from .stage0.effects import bundle as _bundle_mod
from .stage2.llm import _DEFAULT_MODEL as _LLM_DEFAULT_MODEL

if TYPE_CHECKING:
    from .types import ScriptMap


def _emit(progress, **kwargs) -> None:
    if progress is not None:
        from .types import ProgressEvent
        progress(ProgressEvent(**kwargs))


def _make_syntax_error_report(
    entities: dict,
    exc: SyntaxError,
    entity_line_map: dict[str, tuple[int, int]],
) -> "ScoreReport":
    """Return a 0.0-score ScoreReport carrying a SYNTAX FeedbackItem.

    Used when the assembled Python source fails ast.parse() so we avoid
    running the sandbox on provably broken code.
    """
    from .types import ScoreReport, EntityScore, FeedbackItem, EffectClass

    # Find the entity whose declared line range contains the SyntaxError line.
    err_line = exc.lineno or 0
    target_eid = ""
    for eid, (start, end) in entity_line_map.items():
        if start <= err_line <= end:
            target_eid = eid
            break
    if not target_eid and entities:
        target_eid = next(iter(entities))   # fallback: blame the first entity

    score_table = {
        eid: EntityScore(entity_id=eid, executed_ok=False)
        for eid in entities
    }
    feedback = [FeedbackItem(
        entity_id=target_eid,
        effect_class=EffectClass.SYNTAX,
        message=f"SyntaxError at line {exc.lineno}: {exc.msg}",
        score=0.0,
    )]
    return ScoreReport(
        aggregate=0.0,
        by_entity=score_table,
        feedback=feedback,
        py_exit_code=1,
    )


def _state_hash(translation: str) -> str:
    """SHA-256 of the Python source text — tabu key for the visited set."""
    return hashlib.sha256(translation.encode()).hexdigest()


def _top_k(candidates: list[Candidate], k: int) -> list[Candidate]:
    """Return the k highest-scoring candidates.

    sorted() is stable, so incumbents (appearing earlier in the input list)
    beat survivors at equal scores — implements 'prefer_incumbent_on_tie'.
    """
    return sorted(candidates, key=lambda c: c.score, reverse=True)[:k]


def run_loop(
    script_map: "ScriptMap",
    library,
    *,
    max_iters: int = 8,
    score_threshold: float = 0.85,
    beam_width: int = 4,
    use_judge: bool = False,
    data_compare: str = "auto",
    no_seeds: bool = False,
    learned_retrieval: bool = False,
    learned_policy: bool = False,
    output_dir: "Path | None" = None,
    checkpoint_path: "Path | None" = None,
    model: str = _LLM_DEFAULT_MODEL,
    progress=None,
    retranslation_patience: int = 3,
    seed_translation: "str | None" = None,
    **verify_kwargs,
) -> TranslateResult:
    """Run the beam/strict-improvement loop (§4.1).

    Args:
        script_map: Stage 1 ScriptMap for the R source.
        library: PatternLibrary (read by Stage 2, written on evidence/contradiction).
        max_iters: Maximum number of edit iterations.
        score_threshold: Stop early when best beam score reaches this value.
        beam_width: Number of candidates to keep in the beam (W=1 = hill-climbing).
        use_judge: Enable LLM judge fallback (D4, off by default).
        data_compare: "auto" | "exact" | "embedding" (§7.3.1).
        no_seeds: Ignore seed:true patterns (§6.7 transfer experiment).
        learned_retrieval: Use learned retrieval reranker (D6, §12.6 A).
        learned_policy: Use learned edit policy / contextual bandit (D6, §12.6 B).
        output_dir: If set, write edits.log.jsonl and library_diff.json here.
        **verify_kwargs: Forwarded to stage4.verify() (e.g. rtol, atol, timeout_s).
    """
    from . import stage2, stage3, stage4
    from .stage2.stitch import rebuild_entity_line_map as _rebuild
    from .stage3.history import EditHistory
    from .library.epistemology import review as _ep_review
    from .library.retrieval import entity_ast_shape_hash as _shape_hash

    # Configure optional learned components on the library instance (D6).
    # Graceful: PatternLibrary accepts these as attributes; older stubs ignore them.
    _set_attr(library, "learned_retrieval", learned_retrieval)
    _set_attr(library, "learned_policy", learned_policy)

    script_id = hashlib.sha1(script_map.source.encode()).hexdigest()[:12]

    # Count this translation against the run-based archival thresholds.
    if hasattr(library, "index") and hasattr(library.index, "increment_runs"):
        library.index.increment_runs()

    # --- seed translation -------------------------------------------------- #
    from .stage2.stitch import rebuild_entity_line_map as _rebuild
    if seed_translation is not None:
        seed = seed_translation
        entity_line_map = _rebuild(seed)
        if not entity_line_map:
            import warnings
            warnings.warn(
                "resume: no r2py entity sentinels found in existing file — "
                "entity-level targeting will be disabled for this run.",
                stacklevel=2,
            )
    else:
        seed, entity_line_map = stage2.translate(script_map, library, no_seeds=no_seeds, model=model)
    _need_bundles = output_dir is not None
    entities = getattr(script_map, "entities", {})

    # Skip the sandbox entirely if the assembled source is not valid Python.
    try:
        _ast_mod.parse(seed)
        seed_result = stage4.verify(
            script_map, seed,
            data_compare=data_compare, use_judge=use_judge,
            entity_line_map=entity_line_map,
            return_bundle=_need_bundles,
            **verify_kwargs,
        )
        if _need_bundles:
            seed_decomp, seed_py_bundle = seed_result
            _out = Path(output_dir)
            _write_effect_bundle(_out, "r", stage4.get_r_bundle(script_map))
            _write_effect_bundle(_out, "py.0", seed_py_bundle)
            _write_score_report(_out, 0, seed_decomp)
        else:
            seed_decomp = seed_result
    except SyntaxError as _syn_exc:
        seed_decomp = _make_syntax_error_report(entities, _syn_exc, entity_line_map)
        if _need_bundles:
            from .stage0.effects.bundle import EffectBundle as _EB
            seed_py_bundle = _EB(exit_code=1)
            _out = Path(output_dir)
            _write_effect_bundle(_out, "r", stage4.get_r_bundle(script_map))
            _write_effect_bundle(_out, "py.0", seed_py_bundle)
            _write_score_report(_out, 0, seed_decomp)

    _emit(progress, kind="seed_done", score=seed_decomp.aggregate)

    # Monotonically increasing counter for score_report artifact filenames.
    # Avoids collisions when beam_width > 1 produces multiple proposals per iteration.
    _report_idx = 1

    beam: list[Candidate] = [Candidate(seed, seed_decomp.aggregate, seed_decomp)]
    visited: set[str] = {_state_hash(seed)}
    score_history = [seed_decomp]
    # Plateau / retranslation tracking.
    _stall_count = 0
    _last_improvement_score = seed_decomp.aggregate
    _retranslation_count = 0
    _MAX_RETRANSLATIONS = 2
    evidence_added: list[str] = []
    contradictions_added: list[str] = []
    # Per-parent edit histories keyed by state hash so beam members A and B
    # can independently propose the same edit kind (applying it to their
    # different translations produces different states; the tabu set catches
    # actual duplicates).
    histories: dict[str, EditHistory] = {}
    # D6 data logging: collected throughout the run, written to output_dir at end.
    all_episodes: list = []
    all_transitions: list = []
    # Beam members whose entity edit-space is fully exhausted (all entities tried
    # _MAX_ATTEMPTS_PER_ENTITY times with no viable untried edit). These are pruned
    # from future iterations so the loop doesn't stall re-proposing for dead parents.
    exhausted_parents: set[str] = set()

    i = 0
    for i in range(max_iters):
        best = max(beam, key=lambda c: c.score)
        if best.score >= score_threshold:
            break

        # Plateau detection: only count non-crashing iterations toward stall.
        best_crashed = best.decomp.py_exit_code != 0
        if best.score > _last_improvement_score:
            _last_improvement_score = best.score
            _stall_count = 0
        else:
            _stall_count += 1

        # Retranslate from scratch when stuck on a plateau.
        if (
            retranslation_patience > 0
            and _stall_count >= retranslation_patience
            and _retranslation_count < _MAX_RETRANSLATIONS
        ):
            _stall_count = 0
            _retranslation_count += 1
            prior_failures: dict[str, list[str]] = {}
            for fi in best.decomp.feedback:
                prior_failures.setdefault(fi.entity_id, []).append(
                    f"{fi.effect_class.value}: {fi.message}"
                )
            _emit(progress, kind="retranslation_start", iteration=i,
                  score=best.score)
            try:
                retry_src, retry_elmap = stage2.translate(
                    script_map, library,
                    no_seeds=no_seeds, model=model,
                    prior_failures=prior_failures,
                )
                retry_hash = _state_hash(retry_src)
                if retry_hash not in visited:
                    visited.add(retry_hash)
                    try:
                        _ast_mod.parse(retry_src)
                        retry_decomp = stage4.verify(
                            script_map, retry_src,
                            data_compare=data_compare, use_judge=use_judge,
                            entity_line_map=retry_elmap,
                            **verify_kwargs,
                        )
                    except SyntaxError as _syn:
                        retry_decomp = _make_syntax_error_report(
                            entities, _syn, retry_elmap
                        )
                    score_history.append(retry_decomp)
                    retry_candidate = Candidate(retry_src, retry_decomp.aggregate, retry_decomp)
                    beam = _top_k(beam + [retry_candidate], beam_width)
                    _emit(progress, kind="retranslation_done", iteration=i,
                          score=retry_decomp.aggregate)
            except Exception:
                pass  # retranslation failed; continue with existing beam

        active_beam = [p for p in beam if _state_hash(p.translation) not in exhausted_parents]
        if not active_beam:
            break

        _emit(progress, kind="iteration_start", iteration=i, score=best.score)

        proposals: list[Proposal] = []
        # Parallel lists — same index maps collector/transition to its proposal.
        proposal_collectors: list[EpisodeCollector] = []
        proposal_transitions: list["PolicyTransition | None"] = []
        proposal_parent_hashes: list[str] = []
        proposal_parent_decomps: list = []
        for parent in active_beam:
            parent_hash = _state_hash(parent.translation)
            parent_history = histories.setdefault(parent_hash, EditHistory())
            collector = EpisodeCollector()
            try:
                edit = stage3.propose_edit(
                    parent, library,
                    script_map=script_map,
                    history=parent_history,
                    iteration=i,
                    model=model,
                    _collector=collector,
                )
            except RuntimeError:
                exhausted_parents.add(parent_hash)
                continue  # all entities exhausted for this parent

            # Record before the tabu check so Stage 3 won't re-propose an edit
            # that leads to an already-visited state.
            parent_history.add(edit)

            candidate_src = stage3.apply_edit(parent.translation, edit)
            h = _state_hash(candidate_src)
            if h in visited:
                continue
            visited.add(h)

            # Skip sandbox if the edited source is not syntactically valid Python.
            _candidate_elmap = _rebuild(candidate_src)
            try:
                _ast_mod.parse(candidate_src)
            except SyntaxError as _syn_exc:
                new_decomp = _make_syntax_error_report(
                    getattr(script_map, "entities", {}), _syn_exc, _candidate_elmap,
                )
                proposals.append(
                    Proposal(candidate_src, 0.0, new_decomp, edit, parent.score)
                )
                proposal_collectors.append(collector)
                proposal_transitions.append(None)
                proposal_parent_hashes.append(parent_hash)
                proposal_parent_decomps.append(parent.decomp)
                continue

            iter_result = stage4.verify(
                script_map, candidate_src,
                changed=edit.entity_ids,
                data_compare=data_compare,
                use_judge=use_judge,
                entity_line_map=_candidate_elmap,
                return_bundle=_need_bundles,
                **verify_kwargs,
            )
            if _need_bundles:
                new_decomp, iter_py_bundle = iter_result
                _out = Path(output_dir)
                _write_effect_bundle(_out, f"py.{_report_idx}", iter_py_bundle)
                _write_score_report(_out, _report_idx, new_decomp)
            else:
                new_decomp = iter_result
            _report_idx += 1
            proposals.append(
                Proposal(candidate_src, new_decomp.aggregate, new_decomp, edit, parent.score)
            )
            proposal_collectors.append(collector)
            proposal_parent_decomps.append(parent.decomp)

            # Build PolicyTransition directly (bandit data; no stage3 hook needed).
            eid = edit.entity_ids[0] if edit.entity_ids else ""
            es = parent.decomp.by_entity.get(eid)
            tr: "PolicyTransition | None" = None
            if es is not None:
                entity = getattr(script_map, "entities", {}).get(eid)
                exploit = collector.episodes[0].exploit_mode if collector.episodes else False
                tr = PolicyTransition(
                    entity_id=eid,
                    entity_kind=getattr(getattr(entity, "kind", None), "value", ""),
                    package=getattr(entity, "package", None) or "",
                    type_match=es.type_match,
                    control_flow_match=es.control_flow_match,
                    data_output=es.data_output,
                    variable_output=es.variable_output,
                    callable_output=es.callable_output,
                    side_effects=es.side_effects,
                    edit_kind=edit.kind.value,
                    exploit_mode=exploit,
                    outcome=None,   # stamped below
                    score_delta=None,
                    script_id=script_id,
                    iteration=i,
                )
            proposal_transitions.append(tr)
            proposal_parent_hashes.append(parent_hash)

        if not proposals:
            # Break only when every beam member is exhausted (no valid edits remain).
            # If tabu filtering caused empty proposals, the next iteration will use
            # the updated history to try different edits.
            remaining = [p for p in beam if _state_hash(p.translation) not in exhausted_parents]
            if not remaining:
                break

        score_history.extend(p.new_decomp for p in proposals)

        for idx, p in enumerate(proposals):
            if p.new_score > p.parent_score:
                outcome = "accepted"
                delta = p.new_score - p.parent_score
                # Carry the parent's edit history forward so the new candidate
                # doesn't re-propose edits that already failed on the parent state.
                new_hash = _state_hash(p.candidate)
                if new_hash not in histories:
                    parent_hist = histories.get(proposal_parent_hashes[idx])
                    histories[new_hash] = EditHistory(
                        tried=list(parent_hist.tried) if parent_hist else []
                    )
                _eid = p.edit.entity_ids[0] if p.edit.entity_ids else ""
                _ent = getattr(script_map, "entities", {}).get(_eid)
                _hash = _shape_hash(_ent) if _ent is not None else ""
                _pkg = getattr(_ent, "package", "") or "" if _ent is not None else ""
                _r_snip = _entity_r_snippet(_ent, script_map)
                _candidate_elmap_ex = _rebuild(p.candidate)
                _py_snip = _extract_entity_snippet(p.candidate, _candidate_elmap_ex, _eid)
                _parent_decomp_ex = (
                    proposal_parent_decomps[idx]
                    if idx < len(proposal_parent_decomps) else None
                )
                _fail_cls = _dominant_failure_class(
                    getattr(_parent_decomp_ex, "feedback", []), _eid
                )
                _old_code, _new_code = _edit_code_pair(p.edit)
                library.record_evidence(
                    p.edit,
                    score_delta=delta,
                    script_id=script_id,
                    ast_shape_hash=_hash,
                    entity_package=_pkg,
                    r_snippet=_r_snip,
                    py_snippet=_py_snip,
                    failure_class=_fail_cls,
                    old_code=_old_code,
                    new_code=_new_code,
                )
                if p.edit.pattern_id:
                    evidence_added.append(p.edit.pattern_id)
            elif p.new_score == p.parent_score:
                outcome = "tie"
                delta = 0.0
                library.record_tie(p.edit, script_id=script_id)
            else:
                outcome = "rejected"
                delta = p.new_score - p.parent_score
                library.record_contradiction(
                    p.edit, observed=p.new_score, script_id=script_id,
                )
                if p.edit.pattern_id:
                    contradictions_added.append(p.edit.pattern_id)

            _emit(progress, kind="proposal", iteration=i,
                  edit_kind=p.edit.kind.value,
                  entity_id=p.edit.entity_ids[0] if p.edit.entity_ids else "",
                  score=p.new_score, outcome=outcome)

            # Stamp outcome onto retrieval episodes from this proposal.
            for ep in proposal_collectors[idx].episodes:
                ep.outcome = outcome
                ep.score_delta = delta
                ep.script_id = script_id
                ep.iteration = i
            all_episodes.extend(proposal_collectors[idx].episodes)

            # Stamp and collect the matching PolicyTransition (parallel to proposals).
            tr = proposal_transitions[idx]
            if tr is not None:
                tr.outcome = outcome
                tr.score_delta = delta
                all_transitions.append(tr)

        beam_min = min(c.score for c in beam)
        # When the entire beam is in a crashed state, also accept tie proposals.
        # Fixing a crash often requires a chain of edits where each step doesn't
        # move the aggregate score — the strict > beam_min guard would discard
        # these intermediate states and exhaust the edit budget against a single
        # stuck parent. The tabu set and max_iters remain as backstops.
        survivors = [
            Candidate(p.candidate, p.new_score, p.new_decomp)
            for p in proposals
            if p.new_score > beam_min
            or (best_crashed and p.new_score == beam_min)
        ]
        beam = _top_k(beam + survivors, beam_width)

        if checkpoint_path is not None:
            _write_checkpoint(checkpoint_path, i, max(beam, key=lambda c: c.score).translation)

    # Epistemology review runs unconditionally at end of every loop so that
    # promotion and archival fire even on runs that made no library changes
    # (e.g. a high-scoring translation that needed no edits).  The cost is one
    # store.load_all() per run — acceptable given the library is small.
    try:
        _ep_review(library.store, library.index)
    except Exception:
        pass

    # Write per-run data files (§12.3) when an output_dir is provided.
    if output_dir is not None:
        _write_run_logs(
            Path(output_dir),
            all_episodes,
            all_transitions,
            evidence_added,
            contradictions_added,
        )

    best = max(beam, key=lambda c: c.score)
    _emit(progress, kind="done", score=best.score, iteration=i + 1)

    if checkpoint_path is not None and best.decomp.py_exit_code == 0:
        _delete_checkpoints(checkpoint_path, i)

    return TranslateResult(
        python_source=best.translation,
        final_score=best.score,
        iterations=i + 1,
        score_history=score_history,
        pattern_evidence_added=list(dict.fromkeys(evidence_added)),
        pattern_contradictions_added=list(dict.fromkeys(contradictions_added)),
        final_exit_code=best.decomp.py_exit_code,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _set_attr(obj: object, name: str, value: object) -> None:
    """Set an attribute on obj when it exists; silently skip otherwise."""
    try:
        setattr(obj, name, value)
    except (AttributeError, TypeError):
        pass


def _score_report_to_dict(report) -> dict:
    """Convert ScoreReport to a JSON-serialisable plain dict."""
    return {
        "aggregate": report.aggregate,
        "by_entity": {
            eid: {
                "entity_id": es.entity_id,
                "executed_ok": es.executed_ok,
                "type_match": es.type_match,
                "control_flow_match": es.control_flow_match,
                "data_output": es.data_output,
                "variable_output": es.variable_output,
                "callable_output": es.callable_output,
                "side_effects": es.side_effects,
                "judge_pass": es.judge_pass,
            }
            for eid, es in report.by_entity.items()
        },
        "by_effect": {ec.value: score for ec, score in report.by_effect.items()},
        "uncomparable": report.uncomparable,
        "py_exit_code": report.py_exit_code,
    }


def _write_score_report(out_dir: Path, iteration: int, report) -> None:
    """Write score_report.{iteration}.json to out_dir (§12.3)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"score_report.{iteration}.json"
    path.write_text(json.dumps(_score_report_to_dict(report), indent=2), encoding="utf-8")


def _write_effect_bundle(out_dir: Path, suffix: str, bundle: "EffectBundle") -> None:
    """Write effect_bundle.{suffix}.json to out_dir (§12.3)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"effect_bundle.{suffix}.json"
    path.write_text(json.dumps(_bundle_mod.to_json(bundle), indent=2), encoding="utf-8")


def _write_checkpoint(py_path: Path, iteration: int, source: str) -> None:
    """Write the best translation so far as {stem}.iter_{n}.py beside py_path."""
    out = py_path.with_name(f"{py_path.stem}.iter_{iteration}.py")
    out.write_text(source, encoding="utf-8")


def _delete_checkpoints(py_path: Path, last_iter: int) -> None:
    """Delete all {stem}.iter_{n}.py checkpoint files written during this run."""
    for n in range(last_iter + 1):
        p = py_path.with_name(f"{py_path.stem}.iter_{n}.py")
        p.unlink(missing_ok=True)


def _entity_r_snippet(entity: object, script_map: object) -> str:
    """Return the R source text for an entity (capped at 300 chars)."""
    if entity is None:
        return ""
    span = getattr(entity, "source_span", None)
    if span is None:
        return ""
    source = getattr(script_map, "source", "") or ""
    if not source:
        return ""
    lines = source.splitlines()
    start = getattr(span, "start_line", 0)
    end = min(len(lines), getattr(span, "end_line", start) + 1)
    return "\n".join(lines[start:end])[:300]


def _extract_entity_snippet(source: str, elmap: dict, eid: str) -> str:
    """Extract an entity's Python snippet from the assembled source (capped at 600 chars).

    elmap values are 1-based (start, end) inclusive; start points to the sentinel
    comment line, so actual code starts at lines[start] (0-indexed).
    """
    if not eid or eid not in elmap:
        return ""
    start, end = elmap[eid]
    lines = source.splitlines()
    # start is 1-based; lines[start-1] is the sentinel comment — skip it.
    snippet_lines = lines[start:end]   # 0-indexed: [start, end-1] inclusive
    return "\n".join(snippet_lines)[:600]


def _dominant_failure_class(feedback: list, eid: str) -> str:
    """Return the EffectClass.value of the worst-scoring feedback item for eid."""
    entity_fb = [f for f in feedback if getattr(f, "entity_id", "") == eid]
    if not entity_fb:
        return ""
    worst = min(entity_fb, key=lambda f: getattr(f, "score", 1.0))
    ec = getattr(worst, "effect_class", None)
    return getattr(ec, "value", str(ec)) if ec is not None else ""


def _edit_code_pair(edit: "Edit") -> tuple[str, str]:
    """Extract (old_code, new_code) from edit params for structural edit types."""
    from .types import EditKind
    params = getattr(edit, "params", {}) or {}
    if edit.kind == EditKind.RESTRUCTURE_CONTROL_FLOW:
        return str(params.get("old_code", ""))[:300], str(params.get("new_code", ""))[:300]
    if edit.kind == EditKind.REPLACE_CALL:
        return str(params.get("old_call", ""))[:300], str(params.get("new_call", ""))[:300]
    if edit.kind == EditKind.CHANGE_IMPORT:
        return str(params.get("old_import", ""))[:300], str(params.get("new_import", ""))[:300]
    return "", ""


def _write_run_logs(
    out_dir: Path,
    episodes: list,
    transitions: list,
    evidence_added: list[str],
    contradictions_added: list[str],
) -> None:
    """Write edits.log.jsonl and library_diff.json to out_dir (§12.3)."""
    out_dir.mkdir(parents=True, exist_ok=True)

    # edits.log.jsonl — one JSON line per stamped RetrievalEpisode or PolicyTransition
    log_path = out_dir / "edits.log.jsonl"
    with log_path.open("w", encoding="utf-8") as fh:
        for ep in episodes:
            if ep.outcome is None:
                continue
            fh.write(json.dumps(dataclasses.asdict(ep)) + "\n")
        for tr in transitions:
            if tr.outcome is None:
                continue
            fh.write(json.dumps(dataclasses.asdict(tr)) + "\n")

    # library_diff.json — patterns touched during this run
    diff_path = out_dir / "library_diff.json"
    diff_path.write_text(
        json.dumps({
            "evidence_added": list(dict.fromkeys(evidence_added)),
            "contradictions_added": list(dict.fromkeys(contradictions_added)),
        }, indent=2),
        encoding="utf-8",
    )

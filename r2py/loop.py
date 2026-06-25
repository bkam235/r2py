"""Translation loop: cheap path → reasoning agent escalation.

Try a cheap entity-by-entity translation first. If the score is below
threshold, escalate to the reasoning agent which adaptively probes R,
rewrites code, and verifies until the translation is correct.
"""
from __future__ import annotations

import ast as _ast_mod
import hashlib
import json
from pathlib import Path
from typing import TYPE_CHECKING

from .types import TranslateResult
from .stage0.effects import bundle as _bundle_mod
from .stage2.llm import _DEFAULT_MODEL as _LLM_DEFAULT_MODEL

if TYPE_CHECKING:
    from .types import ScriptMap


def _emit(progress, **kwargs) -> None:
    if progress is not None:
        from .types import ProgressEvent
        progress(ProgressEvent(**kwargs))


def _penalise_reviewed(decomp: "ScoreReport") -> "ScoreReport":
    """Cap the aggregate score so a review-failing translation cannot meet threshold."""
    from .types import ScoreReport
    if decomp.aggregate > 0.5:
        import copy
        penalised = copy.copy(decomp)
        penalised.aggregate = min(decomp.aggregate, 0.5)
        return penalised
    return decomp


def _make_syntax_error_report(
    entities: dict,
    exc: SyntaxError,
    entity_line_map: dict[str, tuple[int, int]],
) -> "ScoreReport":
    from .types import ScoreReport, EntityScore, FeedbackItem, EffectClass

    err_line = exc.lineno or 0
    target_eid = ""
    for eid, (start, end) in entity_line_map.items():
        if start <= err_line <= end:
            target_eid = eid
            break
    if not target_eid and entities:
        target_eid = next(iter(entities))

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


def run_loop(
    script_map: "ScriptMap",
    library,
    *,
    max_iters: int = 20,
    score_threshold: float = 0.85,
    use_judge: bool = False,
    data_compare: str = "auto",
    no_seeds: bool = False,
    n_seeds: int = 1,
    output_dir: "Path | None" = None,
    checkpoint_path: "Path | None" = None,
    model: str = _LLM_DEFAULT_MODEL,
    escalation_model: str = _LLM_DEFAULT_MODEL,
    progress=None,
    seed_translation: "str | None" = None,
    timeout_s: float = 60,
    max_stalls: int = 3,
    **verify_kwargs,
) -> TranslateResult:
    """Cheap path → reasoning agent escalation loop.

    1. Generate a seed translation with Stage 2 (cheap model, entity-by-entity).
    2. Verify with Stage 4. If score >= threshold, done.
    3. Otherwise, escalate to the reasoning agent (expensive model) which
       adaptively probes R, rewrites, and verifies until success or budget exhaustion.
    4. Extract patterns from successful agent sessions into the library.
    """
    from . import stage2, stage4
    from .harness.tools import HarnessTools
    from .harness.agent import reason as _reason
    from .stage2.stitch import rebuild_entity_line_map as _rebuild
    from .library.epistemology import review as _ep_review
    from .harness.review import review_translation as _review

    script_id = hashlib.sha1(script_map.source.encode()).hexdigest()[:12]

    if hasattr(library, "index") and hasattr(library.index, "increment_runs"):
        library.index.increment_runs()

    # --- Seed translation -------------------------------------------------- #
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

    _sidecar_fn = (
        f"{checkpoint_path.stem}.r2py_data.json"
        if checkpoint_path is not None else None
    )

    _script_relpath: str | None = None
    if checkpoint_path is not None:
        try:
            _script_relpath = str(checkpoint_path.resolve().relative_to(Path.cwd()))
        except (ValueError, OSError):
            _script_relpath = str(checkpoint_path)

    verify_kwargs["timeout_s"] = timeout_s

    harness = HarnessTools(
        script_map, library,
        data_compare=data_compare,
        timeout_s=timeout_s,
        sidecar_filename=_sidecar_fn or "",
        verify_kwargs=verify_kwargs,
    )

    if seed_translation is None:
        seed, entity_line_map = stage2.translate(
            script_map, library,
            no_seeds=no_seeds, model=model,
            sidecar_filename=_sidecar_fn,
            script_relpath=_script_relpath,
        )

    entities = getattr(script_map, "entities", {})
    _need_bundles = output_dir is not None

    from .stage2.stitch import collect_shim_needed_names as _collect_shim_names
    _shim_expected_names = _collect_shim_names(script_map) if _sidecar_fn else None

    if checkpoint_path is not None:
        _write_data_sidecar(checkpoint_path, script_map)

    # --- Verify seed 1 ----------------------------------------------------- #
    seed, seed_decomp = _verify_seed(
        seed, entity_line_map, script_map, stage4,
        data_compare, use_judge, _need_bundles, output_dir,
        _sidecar_fn, _shim_expected_names, entities, verify_kwargs,
    )

    _emit(progress, kind="seed_done", score=seed_decomp.aggregate)
    _record_seed_translations(seed, seed_decomp, script_map, library, script_id, entity_line_map)

    r_source = getattr(script_map, "source", "") or ""

    # Review seed for rule compliance — only if it would meet threshold
    if seed_decomp.aggregate >= score_threshold:
        _seed_passed, _seed_reason = _review(
            r_source, seed, script_map, model=escalation_model,
        )
        if not _seed_passed:
            print(f"[Review]  Seed FAILED code review: {_seed_reason}")
            seed_decomp = _penalise_reviewed(seed_decomp)

    best_source = seed
    best_decomp = seed_decomp

    # --- Additional seeds (lazy: only when seed 1 is below reseed threshold) #
    if (seed_translation is None
            and n_seeds > 1
            and best_decomp.aggregate < score_threshold):
        for seed_idx in range(2, n_seeds + 1):
            alt_seed, alt_elmap = stage2.translate(
                script_map, library,
                no_seeds=no_seeds, model=model,
                sidecar_filename=_sidecar_fn,
                script_relpath=_script_relpath,
            )
            alt_seed, alt_decomp = _verify_seed(
                alt_seed, alt_elmap, script_map, stage4,
                data_compare, use_judge, False, None,
                _sidecar_fn, _shim_expected_names, entities, verify_kwargs,
            )
            print(f"[Seed {seed_idx}] score: {alt_decomp.aggregate:.3f}")
            _record_seed_translations(
                alt_seed, alt_decomp, script_map, library, script_id, alt_elmap,
            )
            if alt_decomp.aggregate > best_decomp.aggregate:
                if alt_decomp.aggregate >= score_threshold:
                    alt_passed, alt_reason = _review(
                        r_source, alt_seed, script_map, model=escalation_model,
                    )
                    if not alt_passed:
                        print(f"[Review]  Seed {seed_idx} FAILED: {alt_reason}")
                        alt_decomp = _penalise_reviewed(alt_decomp)
                if alt_decomp.aggregate > best_decomp.aggregate:
                    best_source = alt_seed
                    best_decomp = alt_decomp
                    entity_line_map = alt_elmap
            if best_decomp.aggregate >= score_threshold:
                break

    score_history = [best_decomp]

    # --- Cheap path: done if score is good enough -------------------------- #
    if best_decomp.aggregate >= score_threshold:
        _emit(progress, kind="done", score=best_decomp.aggregate, iteration=0)
        _run_epistemology(library, _ep_review)
        if checkpoint_path is not None and best_decomp.py_exit_code == 0:
            _delete_checkpoints(checkpoint_path, 0)
        return _make_result(best_source, best_decomp, 0, score_history)

    # --- Escalate to reasoning agent --------------------------------------- #
    _emit(progress, kind="agent_start", iteration=0, score=best_decomp.aggregate)

    agent_result = _reason(
        current_source=best_source,
        score_report=best_decomp,
        harness=harness,
        script_map=script_map,
        model=escalation_model,
        max_steps=max_iters,
        score_threshold=score_threshold,
        max_stalls=max_stalls,
    )

    if agent_result is not None:
        improved, agent_report = agent_result
        score_history.append(agent_report)
        if agent_report.aggregate > best_decomp.aggregate:
            best_source = improved
            best_decomp = agent_report
            _record_seed_translations(
                improved, agent_report, script_map, library,
                script_id, _rebuild(improved),
            )
            _extract_agent_knowledge(
                harness, seed, improved, script_map, library, escalation_model,
            )

    if checkpoint_path is not None:
        _write_checkpoint(checkpoint_path, 0, best_source)

    _run_epistemology(library, _ep_review)
    _emit(progress, kind="done", score=best_decomp.aggregate, iteration=1)

    if checkpoint_path is not None and best_decomp.py_exit_code == 0:
        _delete_checkpoints(checkpoint_path, 0)

    return _make_result(best_source, best_decomp, 1, score_history)


def _make_result(
    source: str, decomp, iterations: int, score_history: list,
) -> TranslateResult:
    return TranslateResult(
        python_source=source,
        final_score=decomp.aggregate,
        iterations=iterations,
        score_history=score_history,
        final_exit_code=decomp.py_exit_code,
        final_score_report=decomp,
    )


def _verify_seed(
    seed, entity_line_map, script_map, stage4,
    data_compare, use_judge, need_bundles, output_dir,
    sidecar_fn, shim_expected_names, entities, verify_kwargs,
):
    """Verify a seed translation, return (seed, decomp)."""
    from .stage2.stitch import validate_data_shim

    shim_err = validate_data_shim(seed, shim_expected_names)
    if shim_err:
        import warnings
        warnings.warn(f"seed translation has broken data_shim: {shim_err}", stacklevel=2)
    try:
        _ast_mod.parse(seed)
        result = stage4.verify(
            script_map, seed,
            data_compare=data_compare, use_judge=use_judge,
            entity_line_map=entity_line_map,
            return_bundle=need_bundles,
            sidecar_filename=sidecar_fn,
            **verify_kwargs,
        )
        if need_bundles:
            decomp, py_bundle = result
            _out = Path(output_dir)
            _write_effect_bundle(_out, "r", stage4.get_r_bundle(script_map))
            _write_effect_bundle(_out, "py.0", py_bundle)
            _write_score_report(_out, 0, decomp)
        else:
            decomp = result
    except SyntaxError as syn_exc:
        decomp = _make_syntax_error_report(entities, syn_exc, entity_line_map)
        if need_bundles:
            from .stage0.effects.bundle import EffectBundle as _EB
            py_bundle = _EB(exit_code=1)
            _out = Path(output_dir)
            _write_effect_bundle(_out, "r", stage4.get_r_bundle(script_map))
            _write_effect_bundle(_out, "py.0", py_bundle)
            _write_score_report(_out, 0, decomp)
    return seed, decomp


def _extract_agent_knowledge(
    harness,
    original_source: str,
    improved_source: str,
    script_map,
    library,
    model: str,
) -> None:
    """Record probe history and extract agent-articulated insights after success."""
    from .library.writer import record_agent_insight

    r_source = getattr(script_map, "source", "") or ""

    # Record probe history on relevant patterns.
    for expression, result in harness._probe_history:
        probe_note = f"R probe: `{expression}` → `{result[:200]}`"
        for eid, entity in getattr(script_map, "entities", {}).items():
            pkg = getattr(entity, "package", None)
            if not pkg:
                continue
            if entity.name in expression:
                pat_id = f"{pkg}.{entity.name}"
                pat = library.store.get(pat_id)
                if pat is not None and probe_note not in pat.guidance:
                    record_agent_insight(
                        library.store, library.index, pat_id, probe_note,
                        entity_package=pkg,
                    )
                break

    # Extract reusable insights via LLM.
    try:
        from .harness.agent import extract_insights
        insights = extract_insights(
            r_source, original_source, improved_source, model=model,
        )
    except Exception:
        insights = []

    for rule_name, guidance in insights:
        import re as _re
        pat_id = _re.sub(r'[^a-z0-9._-]', '-', rule_name.lower()).strip('-')[:80]
        pkg = ""
        for entity in getattr(script_map, "entities", {}).values():
            if getattr(entity, "package", None):
                pkg = entity.package
                break
        record_agent_insight(
            library.store, library.index, pat_id, guidance,
            entity_package=pkg,
        )


def _run_epistemology(library, review_fn) -> None:
    try:
        review_fn(library.store, library.index)
    except Exception:
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


def _write_data_sidecar(py_path: "Path", script_map: object) -> None:
    """Persist R-captured runtime data as ``{stem}.r2py_data.json`` beside py_path.

    Loaded by the verifier via the data-loading shim (see stage2/stitch.py and
    stage4/verifier.py).  Also serves as a manual-debugging artifact — the user
    can un-comment the shim block in the saved .py and re-run the script
    against the same captured data.

    Idempotent and safe to call repeatedly (data is iteration-invariant).
    """
    try:
        from .stage4.verifier import get_r_bundle
        from .stage0.effects.data import serialize_bundle_data
    except Exception:
        return  # Sidecar is best-effort; never block a translation on this.
    try:
        bundle = get_r_bundle(script_map)
    except Exception:
        return
    data = getattr(bundle, "data", {}) or {}
    if not data:
        return
    entity_names = set(getattr(script_map, "entities", {}) or {})
    filtered = {k: v for k, v in data.items() if k not in entity_names}
    if not filtered:
        return
    sidecar = py_path.with_name(f"{py_path.stem}.r2py_data.json")
    try:
        sidecar.write_text(
            serialize_bundle_data(filtered, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass


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


_SEED_RECORD_THRESHOLD = 0.5  # minimum per-entity avg score to record a TranslationExample


def _entity_score_avg(es) -> float:
    """Average over all six EntityScore fields (same formula as the aggregate)."""
    return (es.type_match + es.control_flow_match + es.data_output
            + es.variable_output + es.callable_output + es.side_effects) / 6


def _packages_compatible(pattern_pkg: str, entity_pkg: str) -> bool:
    """True when a pattern's package is compatible with an entity's package.

    Empty-package patterns (created without package info) match any entity.
    Non-empty packages must match exactly.
    """
    if not pattern_pkg or not entity_pkg:
        return True
    return pattern_pkg == entity_pkg


def _record_seed_translations(
    source: str,
    decomp,
    script_map: object,
    library: object,
    script_id: str,
    entity_line_map: dict,
) -> None:
    """Attach per-entity TranslationExamples to the library from a well-scoring translation.

    Called after the initial seed and after agent success so that entity
    implementations that actually worked are captured.

    Does NOT create new patterns — that is left to seed_from_translation() for
    human-authorised seeding.
    """
    if not hasattr(library, "retrieve") or not hasattr(library, "store"):
        return
    if decomp.aggregate < _SEED_RECORD_THRESHOLD:
        return

    from .library.pattern import TranslationExample, r_snippet_hash
    from .library.writer import _add_translation_example

    entities = getattr(script_map, "entities", {})

    for eid, entity in entities.items():
        es = decomp.by_entity.get(eid)
        if es is None or not es.executed_ok:
            continue
        avg = _entity_score_avg(es)
        if avg < _SEED_RECORD_THRESHOLD:
            continue

        r_snip = _entity_r_snippet(entity, script_map)
        py_snip = _extract_entity_snippet(source, entity_line_map, eid)
        if not r_snip or not py_snip.strip():
            continue
        if py_snip.strip().startswith("pass"):
            continue

        r_hash = r_snippet_hash(r_snip)
        ex = TranslationExample(
            r_hash=r_hash,
            r_snippet=r_snip[:300],
            py_snippet=py_snip[:600],
            score=avg,
            script_id=script_id,
        )

        updated_pids: set[str] = set()

        # Record against retrieved pattern matches.
        entity_pkg = getattr(entity, "package", "") or ""
        patterns = library.retrieve(entity, k=3)
        for pat_obj in patterns:
            if not _packages_compatible(pat_obj.package, entity_pkg):
                continue
            pat = library.store.get(pat_obj.id)
            if pat is None:
                continue
            _add_translation_example(pat, ex)
            library.store.save(pat)
            updated_pids.add(pat_obj.id)

        # Also update any pattern that already has an example with the
        # same r_hash — these were created by record_evidence and may
        # not be returned by retrieve.
        for pid, pat_data in library.store.load_all().items():
            if pid in updated_pids:
                continue
            if any(e.r_hash == r_hash for e in pat_data.translation_examples):
                _add_translation_example(pat_data, ex)
                library.store.save(pat_data)



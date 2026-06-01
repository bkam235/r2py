"""Stage 4 verifier orchestrator (§7.1, §7.4)."""
from __future__ import annotations

import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

from ..stage0.effects import bundle as _bundle_mod
from ..stage0.sandbox.py_sandbox import PySandbox
from ..types import (
    CaptureSpec,
    ComparatorResult,
    EffectBundle,
    EffectClass,
    EntityId,
    FeedbackItem,
    ScoreReport,
)
from .comparators import COMPARATORS
from .comparators.data import DataComparator as _DataComparator
from .decompose import make_score_table

if TYPE_CHECKING:
    from ..stage1.script_map import ScriptMap as _FullScriptMap


# All capturable effect classes for the Python sandbox run.
_ALL_CAPTURE: CaptureSpec = frozenset({
    EffectClass.STDOUT,
    EffectClass.FILES,
    EffectClass.GRAPHICS,
    EffectClass.DATA,
    EffectClass.HTML,
    EffectClass.ENV,
    EffectClass.WARNINGS,
    EffectClass.RNG,
})


def _get_r_bundle(script_map) -> EffectBundle:
    """Aggregate entity actual_bundles from the ScriptMap into one R ground-truth bundle.

    Deduplicates by object identity: all entities produced by Stage 1's main run
    share the same bundle object, so we merge each unique bundle exactly once.
    """
    seen_ids: set[int] = set()
    bundles: list[EffectBundle] = []
    for e in getattr(script_map, "entities", {}).values():
        ab = getattr(e, "actual_bundle", None)
        if ab is not None and id(ab) not in seen_ids:
            seen_ids.add(id(ab))
            bundles.append(ab)
    if bundles:
        return _bundle_mod.merge(bundles)
    # No entity bundles — return empty (all comparators will score as 1.0 empty-vs-empty)
    return EffectBundle()


def _compare_bundles(
    r_bundle: EffectBundle,
    py_bundle: EffectBundle,
    data_compare: str,
    rtol: float,
    atol: float,
) -> dict[EffectClass, ComparatorResult]:
    results: dict[EffectClass, ComparatorResult] = {}

    # STDOUT
    results[EffectClass.STDOUT] = COMPARATORS[EffectClass.STDOUT].compare(
        r_bundle.stdout, py_bundle.stdout
    )

    # WARNINGS
    results[EffectClass.WARNINGS] = COMPARATORS[EffectClass.WARNINGS].compare(
        r_bundle.warnings, py_bundle.warnings
    )

    # ENV
    results[EffectClass.ENV] = COMPARATORS[EffectClass.ENV].compare(
        r_bundle.env, py_bundle.env
    )

    # FILES
    results[EffectClass.FILES] = COMPARATORS[EffectClass.FILES].compare(
        r_bundle.files, py_bundle.files
    )

    # HTML
    results[EffectClass.HTML] = COMPARATORS[EffectClass.HTML].compare(
        r_bundle.html, py_bundle.html
    )

    # GRAPHICS
    results[EffectClass.GRAPHICS] = COMPARATORS[EffectClass.GRAPHICS].compare(
        r_bundle.graphics, py_bundle.graphics
    )

    # DATA — uses configurable data_compare + tolerance
    data_cmp = _DataComparator(data_compare=data_compare, rtol=rtol, atol=atol)
    results[EffectClass.DATA] = data_cmp.compare(
        r_bundle.data, py_bundle.data, uncapturable=py_bundle.uncapturable
    )

    return results


def _build_feedback(
    comparator_results: dict[EffectClass, ComparatorResult],
    entities: dict,
) -> list[FeedbackItem]:
    """Convert comparator results into FeedbackItems for Stage 3.

    Triggers on any partial score (score < 1.0), not just hard "fail", so
    pass_via_fallback results (e.g. score=0.603) generate actionable feedback
    instead of leaving Stage 3 with no signal.

    DATA failures: attributed to the specific entity whose name matches the
    failing variable, so Stage 3 targets the right entity. Non-DATA effects
    are broadcast to all entities (whole-script signal).
    """
    items: list[FeedbackItem] = []

    name_to_eid: dict[str, str] = {
        getattr(e, "name", None): eid
        for eid, e in entities.items()
        if getattr(e, "name", None)
    }

    for ec, result in comparator_results.items():
        if result.score >= 1.0:
            continue

        if ec == EffectClass.DATA and result.per_variable:
            for var_name, var_score in result.per_variable.items():
                if var_score >= 1.0:
                    continue
                expl = (
                    _extract_var_explanation(result.explanation, var_name)
                    or f"{var_name}: score {var_score:.3f}"
                )
                target_eid = name_to_eid.get(var_name)
                if target_eid:
                    items.append(FeedbackItem(
                        entity_id=target_eid,
                        effect_class=ec,
                        message=expl,
                        score=var_score,
                    ))
                else:
                    for eid in entities:
                        items.append(FeedbackItem(
                            entity_id=eid,
                            effect_class=ec,
                            message=expl,
                            score=var_score,
                        ))
        else:
            if not result.explanation:
                continue
            for entity_id in entities:
                items.append(FeedbackItem(
                    entity_id=entity_id,
                    effect_class=ec,
                    message=result.explanation,
                    score=result.score,
                ))

    return items


def _extract_var_explanation(full_explanation: str, var_name: str) -> str | None:
    """Extract the semicolon-delimited fragment for var_name from a joined explanation."""
    for fragment in full_explanation.split(";"):
        fragment = fragment.strip()
        if fragment.startswith(var_name + ":") or fragment.startswith(var_name + "["):
            return fragment
    return None


def get_r_bundle(script_map) -> EffectBundle:
    """Return the aggregated R ground-truth EffectBundle for *script_map*."""
    return _get_r_bundle(script_map)


def verify(
    script_map,
    candidate: str,
    changed: list[str] | None = None,
    data_compare: str = "auto",
    rtol: float = 1e-6,
    atol: float = 1e-9,
    use_fuzz: bool = False,
    fuzz_n: int = 10,
    use_judge: bool = False,
    workdir: Path | None = None,
    timeout_s: float = 60,
    entity_line_map: dict | None = None,
    return_bundle: bool = False,
) -> "ScoreReport | tuple[ScoreReport, EffectBundle]":
    """Score a candidate Python translation against the R ScriptMap.

    changed: entity_ids touched by the last edit; if provided, only those
    entities are re-verified (incremental verification, §7.4).
    """
    entities = getattr(script_map, "entities", {})

    # --- Run candidate in Python sandbox ---
    r_bundle = _get_r_bundle(script_map)

    # Determine which effects were actually captured in R so we capture the same in Python
    capture = _ALL_CAPTURE

    sandbox = PySandbox()
    if workdir is not None:
        py_bundle = sandbox.run(candidate, workdir=workdir, capture=capture, timeout_s=timeout_s)
    else:
        with tempfile.TemporaryDirectory() as _tmpdir:
            py_bundle = sandbox.run(candidate, workdir=Path(_tmpdir), capture=capture, timeout_s=timeout_s)

    # --- Compare bundles ---
    comparator_results = _compare_bundles(r_bundle, py_bundle, data_compare, rtol, atol)

    # --- Score decomposition ---
    score_table = make_score_table(
        entities, comparator_results,
        py_exit_code=py_bundle.exit_code,
        entity_line_map=entity_line_map,
        py_stderr=py_bundle.stderr,
        preamble_lines=py_bundle.preamble_lines,
    )

    # --- Differential fuzzing (optional) ---
    feedback: list[FeedbackItem] = []
    if use_fuzz:
        from . import fuzz as _fuzz
        fuzz_cfg = _fuzz.FuzzConfig(n_inputs=fuzz_n)
        feedback.extend(_fuzz.run_fuzz(script_map, candidate, config=fuzz_cfg, data_compare=data_compare))

    feedback.extend(_build_feedback(comparator_results, entities))

    # RC2: surface crash traceback as feedback so Stage 3 knows what line failed
    if py_bundle.exit_code != 0 and py_bundle.stderr:
        crash_msg = py_bundle.stderr.strip()
        if len(crash_msg) > 800:
            crash_msg = "..." + crash_msg[-800:]
        for entity_id in entities:
            feedback.append(FeedbackItem(
                entity_id=entity_id,
                effect_class=EffectClass.SYNTAX,
                message=f"Python crashed (exit {py_bundle.exit_code}): {crash_msg}",
                score=0.0,
            ))

    # --- Uncomparable entities ---
    uncomparable: list[EntityId] = []
    data_result = comparator_results.get(EffectClass.DATA)
    if data_result and data_result.verdict == "uncomparable":
        uncomparable.extend(entities.keys())

    # --- Aggregate score ---
    # Per entity: average of all six EntityScore fields (kind-aware proxies populated by decompose).
    entity_scores = list(score_table.values())
    if entity_scores:
        per_entity_avgs = [
            (es.type_match + es.control_flow_match + es.data_output
             + es.variable_output + es.callable_output + es.side_effects) / 6
            for es in entity_scores
        ]
        aggregate = sum(per_entity_avgs) / len(per_entity_avgs)
    else:
        # No entities: score the raw effect comparison
        scored_results = [r for r in comparator_results.values() if r.verdict != "uncomparable"]
        aggregate = sum(r.score for r in scored_results) / len(scored_results) if scored_results else 1.0

    by_effect = {ec: result.score for ec, result in comparator_results.items()}

    report = ScoreReport(
        aggregate=aggregate,
        by_entity=score_table,
        by_effect=by_effect,
        uncomparable=uncomparable,
        feedback=feedback,
        py_exit_code=py_bundle.exit_code,
    )
    if return_bundle:
        return report, py_bundle
    return report

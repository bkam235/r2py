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
    """Aggregate entity actual_bundles from the ScriptMap into one R ground-truth bundle."""
    bundles = [
        e.actual_bundle
        for e in getattr(script_map, "entities", {}).values()
        if getattr(e, "actual_bundle", None) is not None
    ]
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
    """Convert comparator failures into FeedbackItems for Stage 3."""
    items: list[FeedbackItem] = []
    for ec, result in comparator_results.items():
        if result.verdict in ("fail",) and result.explanation:
            # One feedback item per failing effect class; entity attribution is
            # whole-script for now (per-entity slicing deferred to Stage 2).
            for entity_id in entities:
                items.append(FeedbackItem(
                    entity_id=entity_id,
                    effect_class=ec,
                    message=result.explanation,
                    score=result.score,
                ))
                break
    return items


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
) -> ScoreReport:
    """Score a candidate Python translation against the R ScriptMap.

    changed: entity_ids touched by the last edit; if provided, only those
    entities are re-verified (incremental verification, §7.4).
    """
    entities = getattr(script_map, "entities", {})
    if changed is not None:
        entities = {eid: e for eid, e in entities.items() if eid in changed}

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
    score_table = make_score_table(entities, comparator_results, py_exit_code=py_bundle.exit_code)

    # --- Differential fuzzing (optional) ---
    feedback: list[FeedbackItem] = []
    if use_fuzz:
        from . import fuzz as _fuzz
        fuzz_cfg = _fuzz.FuzzConfig(n_inputs=fuzz_n)
        feedback.extend(_fuzz.run_fuzz(script_map, candidate, config=fuzz_cfg, data_compare=data_compare))

    feedback.extend(_build_feedback(comparator_results, entities))

    # --- Uncomparable entities ---
    uncomparable: list[EntityId] = []
    data_result = comparator_results.get(EffectClass.DATA)
    if data_result and data_result.verdict == "uncomparable":
        uncomparable.extend(entities.keys())

    # --- Aggregate score ---
    # Per entity: average of data_output + side_effects (type/control not yet populated)
    entity_scores = list(score_table.values())
    if entity_scores:
        per_entity_avgs = [
            (es.data_output + es.side_effects) / 2
            for es in entity_scores
        ]
        aggregate = sum(per_entity_avgs) / len(per_entity_avgs)
    else:
        # No entities: score the raw effect comparison
        scored_results = [r for r in comparator_results.values() if r.verdict != "uncomparable"]
        aggregate = sum(r.score for r in scored_results) / len(scored_results) if scored_results else 1.0

    by_effect = {ec: result.score for ec, result in comparator_results.items()}

    return ScoreReport(
        aggregate=aggregate,
        by_entity=score_table,
        by_effect=by_effect,
        uncomparable=uncomparable,
        feedback=feedback,
    )

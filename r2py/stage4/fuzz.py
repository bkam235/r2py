"""Differential fuzzing harness (§7.8).

Strengthens single-path equivalence by running R (oracle) and Python on many
derived inputs and requiring their effect bundles to match on each.

Inputs are derived from observed types, not invented by an LLM.
"""
from __future__ import annotations

import logging
import random
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

_log = logging.getLogger(__name__)

from ..stage0.sandbox.py_sandbox import PySandbox
from ..stage1 import runner as _r_runner
from ..types import CaptureSpec, EffectBundle, EffectClass, FeedbackItem
from .comparators.data import DataComparator
from .generators import generator_from_observed


@dataclass
class FuzzConfig:
    n_inputs: int = 10       # random samples per entity
    seed: int = 42
    timeout_s: float = 30    # per-run timeout in seconds


def _inject_input(source: str, var_name: str, value: object) -> str:
    """Prepend a variable assignment to a source snippet."""
    if isinstance(value, str):
        literal = repr(value)
    elif isinstance(value, bool):
        literal = "TRUE" if value else "FALSE"
    elif value is None:
        literal = "NULL"
    elif isinstance(value, list):
        inner = ", ".join(
            "NULL" if v is None else ("TRUE" if v is True else "FALSE" if v is False else repr(v))
            for v in value
        )
        literal = f"c({inner})"
    elif isinstance(value, dict):
        # data.frame-style dict → data.frame(col=c(...), ...)
        cols = []
        for col, vals in value.items():
            if isinstance(vals, list):
                inner = ", ".join(repr(v) if v is not None else "NA" for v in vals)
                cols.append(f"{col}=c({inner})")
        literal = f"data.frame({', '.join(cols)})"
    else:
        literal = repr(value)
    return f"{var_name} <- {literal}\n" + source


def _inject_py_input(source: str, var_name: str, value: object) -> str:
    """Prepend a Python variable assignment to a source snippet."""
    if isinstance(value, list):
        literal = repr(value)
    elif isinstance(value, dict):
        # dict-of-columns → pandas DataFrame if pandas available, else plain dict
        literal = f"_r2py_fuzz_df = {repr(value)}\ntry:\n    import pandas as _pd\n    {var_name} = _pd.DataFrame(_r2py_fuzz_df)\nexcept ImportError:\n    {var_name} = _r2py_fuzz_df\n"
        return literal + source
    else:
        literal = repr(value)
    return f"{var_name} = {literal}\n" + source


def _run_python_slice(source: str, workdir: Path, timeout_s: float) -> EffectBundle:
    capture: CaptureSpec = frozenset({EffectClass.DATA, EffectClass.STDOUT})
    sandbox = PySandbox()
    return sandbox.run(source, workdir=workdir, capture=capture, timeout_s=timeout_s)


def run_fuzz(
    script_map,
    candidate: str,
    config: FuzzConfig | None = None,
    data_compare: str = "auto",
) -> list[FeedbackItem]:
    """Run differential fuzzing over entities with observed data inputs.

    Returns a list of FeedbackItems for the first counterexample found per entity.
    """
    if config is None:
        config = FuzzConfig()
    entities = getattr(script_map, "entities", {})
    rng = random.Random(config.seed)
    cmp = DataComparator(data_compare=data_compare)
    feedback: list[FeedbackItem] = []

    for entity_id, entity in entities.items():
        bundle = getattr(entity, "actual_bundle", None)
        if bundle is None or not bundle.data:
            continue

        # Use the entity's observed data as the free-input domain
        for var_name, observed_value in bundle.data.items():
            gen = generator_from_observed(observed_value)

            # Boundary cases first, then random samples
            inputs = gen.boundary_cases() + [gen.sample(rng) for _ in range(config.n_inputs)]

            for inp in inputs:
                # Build R slice and Python slice with the injected input
                r_slice = getattr(entity, "runnable_slice", None) or script_map.source
                r_source_with_input = _inject_input(r_slice, var_name, inp)
                py_source_with_input = _inject_py_input(candidate, var_name, inp)

                # Run R oracle
                try:
                    r_bundle = _r_runner.run_slice(r_source_with_input)
                except Exception as exc:
                    _log.debug("fuzz: R slice failed for %s=%r: %s", var_name, inp, exc)
                    continue

                # Run Python candidate
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        py_bundle = _run_python_slice(
                            py_source_with_input, Path(tmpdir), config.timeout_s
                        )
                except Exception as exc:
                    _log.debug("fuzz: Python slice failed for %s=%r: %s", var_name, inp, exc)
                    continue

                # Compare data outputs
                result = cmp.compare(r_bundle.data, py_bundle.data, uncapturable=py_bundle.uncapturable)

                if result.verdict in ("fail",):
                    feedback.append(FeedbackItem(
                        entity_id=entity_id,
                        effect_class=EffectClass.DATA,
                        message=(
                            f"fuzz counterexample for '{var_name}'={inp!r}: {result.explanation}"
                        ),
                        score=result.score,
                    ))
                    break  # first counterexample per entity

    return feedback

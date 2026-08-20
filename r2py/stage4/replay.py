"""RNG capture/replay for unevaluated branches (§7.5)."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from ..stage0.sandbox.base import ReplayLog as _SandboxReplayLog
from ..stage0.sandbox.py_sandbox import PySandbox
from ..types import EffectBundle


@dataclass
class ReplayLog:
    """Extracted RNG sequence from an R run, ready to inject into Python."""
    rng_sequence: list[float] = field(default_factory=list)


def capture_r_rng(r_bundle: EffectBundle) -> ReplayLog:
    """Extract drawn float values from an R bundle's rng_log for Python replay."""
    return ReplayLog(
        rng_sequence=[t[2] for t in r_bundle.rng_log if isinstance(t[2], float)]
    )


def _build_sandbox_replay(log: ReplayLog) -> _SandboxReplayLog:
    """Convert our ReplayLog to the Stage 0 sandbox's ReplayLog format."""
    draws = [("replay", (), v) for v in log.rng_sequence]
    return _SandboxReplayLog(rng_draws=draws)


def run_branch_pair(
    r_branch_bundle: EffectBundle,
    py_slice_source: str,
    py_sandbox: PySandbox,
    workdir: Path,
    timeout_s: float = 30,
) -> tuple[EffectBundle, EffectBundle]:
    """Run a Python branch slice with R's RNG sequence replayed.

    Returns (r_branch_bundle, py_branch_bundle). The R bundle is already
    provided (computed by stage1.runner.run_slice); this function only runs
    the Python side with RNG replay injected.
    """
    from ..types import CaptureSpec, EffectClass
    capture: CaptureSpec = frozenset({
        EffectClass.STDOUT,
        EffectClass.DATA,
        EffectClass.ENV,
        EffectClass.WARNINGS,
    })
    replay_log = capture_r_rng(r_branch_bundle)
    sandbox_replay = _build_sandbox_replay(replay_log)

    py_bundle = py_sandbox.run(
        py_slice_source,
        workdir=workdir,
        capture=capture,
        replay=sandbox_replay,
        timeout_s=timeout_s,
    )
    return r_branch_bundle, py_bundle

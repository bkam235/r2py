"""Sandbox protocol and shared types (§2.3)."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, runtime_checkable

from ...types import CaptureSpec, EffectBundle


@dataclass
class ReplayLog:
    """Pre-recorded side-effect log used for deterministic replay runs (§2.3).

    Injected into sandbox preambles to stub out non-deterministic calls so a
    script can be re-run and produce identical effects to a prior capture.
    """
    rng_draws: list[tuple] = field(default_factory=list)      # (fn, args, value)
    network_stubs: list[tuple] = field(default_factory=list)  # (verb, target, response)
    io_stubs: list[tuple] = field(default_factory=list)       # (call, args, return_val)


class SandboxEscape(RuntimeError):
    """Raised when a script writes files outside its isolated workdir (§2.2)."""


@runtime_checkable
class Sandbox(Protocol):
    """Protocol implemented by RSandbox and PySandbox (§2.3).

    A Sandbox runs one script in an isolated workdir, captures the requested
    effect classes, and returns an EffectBundle.  The caller controls isolation;
    the sandbox must not mutate global state.
    """

    def run(
        self,
        source: str,
        *,
        workdir: Path,
        capture: CaptureSpec,
        preamble: str = "",
        epilogue: str = "",
        seed: int | None = None,
        replay: ReplayLog | None = None,
        timeout_s: float = 60,
    ) -> EffectBundle: ...

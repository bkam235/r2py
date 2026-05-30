"""Rscript subprocess sandbox (§2.3)."""
from __future__ import annotations

import subprocess
import time
from pathlib import Path

from ...types import CaptureSpec, EffectBundle, EffectClass
from ..effects import data as _data_effects
from ..effects import env as _env_effects
from ..effects import files as _files_effects
from ..effects import graphics as _graphics_effects
from ..effects import html as _html_effects
from ..effects import network as _network_effects
from ..effects import rng as _rng_effects
from ..effects import stdout as _stdout_effects
from ..effects import warnings as _warnings_effects
from ..env.r_runtime import find_rscript
from .base import ReplayLog, SandboxEscape
from .isolation import TempWorkdir, check_escape, scrub_env, snapshot_home


class RSandbox:
    """Run R scripts in an isolated subprocess, capturing requested effects."""

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
    ) -> EffectBundle:
        rscript = find_rscript()

        # Build capture preambles/epilogues in addition to caller-supplied ones.
        pre_parts: list[str] = []
        epi_parts: list[str] = []

        if seed is not None:
            pre_parts.append(f"set.seed({seed}L)\n")

        if EffectClass.DATA in capture:
            pre_parts.append(_data_effects.R_PREAMBLE)
            epi_parts.append(_data_effects.build_r_epilogue())

        if EffectClass.GRAPHICS in capture:
            pre_parts.append(_graphics_effects.R_PREAMBLE)
            epi_parts.append(_graphics_effects.R_EPILOGUE)

        if EffectClass.HTML in capture:
            epi_parts.append(_html_effects.R_EPILOGUE)

        if EffectClass.ENV in capture:
            pre_parts.append(_env_effects.R_PREAMBLE)
            epi_parts.append(_env_effects.R_EPILOGUE)

        if EffectClass.WARNINGS in capture:
            pre_parts.append(_warnings_effects.R_PREAMBLE_SIMPLE)
            epi_parts.append(_warnings_effects.R_EPILOGUE_SIMPLE)

        if EffectClass.RNG in capture:
            pre_parts.append(_rng_effects.r_preamble(seed=seed, replay=replay))
            epi_parts.append(_rng_effects.R_EPILOGUE_CAPTURE)

        if EffectClass.NETWORK in capture:
            pre_parts.append(_network_effects.R_PREAMBLE)
            epi_parts.append(_network_effects.R_EPILOGUE)

        # Snapshot workdir before run (for files diff)
        before_files = _files_effects.snapshot(workdir) if EffectClass.FILES in capture else {}

        # Snapshot home for escape detection
        home_snap = snapshot_home()

        # Assemble the full script
        full_script = (
            "\n".join(pre_parts)
            + "\n"
            + preamble
            + "\n"
            + source
            + "\n"
            + epilogue
            + "\n"
            + "\n".join(epi_parts)
        )

        # Write to workdir
        script_path = workdir / "_r2py_script.R"
        script_path.write_text(full_script, encoding="utf-8")

        t_start = time.monotonic()
        result = subprocess.run(
            [str(rscript), "--vanilla", str(script_path)],
            cwd=str(workdir),
            capture_output=True,
            timeout=timeout_s,
            env=scrub_env(),
        )
        run_time = time.monotonic() - t_start

        # Escape detection
        check_escape(home_snap, workdir)

        # Assemble EffectBundle
        bundle = EffectBundle(exit_code=result.returncode, run_time_s=run_time)

        # Always collect stdout/stderr — they're free from the subprocess streams.
        collected = _stdout_effects.collect(result.stdout, result.stderr)
        bundle.stdout = collected["stdout"]
        bundle.stderr = collected["stderr"]

        if EffectClass.FILES in capture:
            collected = _files_effects.collect(workdir, before_files)
            bundle.files = collected["files"]

        if EffectClass.GRAPHICS in capture:
            collected = _graphics_effects.collect(workdir)
            bundle.graphics = collected["graphics"]

        if EffectClass.DATA in capture:
            collected = _data_effects.collect(workdir)
            bundle.data = collected["data"]
            bundle.uncapturable.extend(collected.get("uncapturable", []))

        if EffectClass.HTML in capture:
            collected = _html_effects.collect(workdir)
            bundle.html = collected["html"]

        if EffectClass.ENV in capture:
            collected = _env_effects.collect(workdir)
            bundle.env = collected["env"]

        if EffectClass.WARNINGS in capture:
            collected = _warnings_effects.collect(workdir)
            bundle.warnings = collected["warnings"]

        if EffectClass.RNG in capture:
            collected = _rng_effects.collect(workdir)
            bundle.rng_log = collected["rng_log"]

        if EffectClass.NETWORK in capture:
            collected = _network_effects.collect(workdir)
            bundle.network_log = collected.get("network_log", [])

        return bundle

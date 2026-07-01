"""Python subprocess sandbox (§2.3)."""
from __future__ import annotations

import re
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
from ..env.py_runtime import find_python
from .base import ReplayLog
from .isolation import check_escape, scrub_env, snapshot_home

_MISSING_MODULE_RE = re.compile(
    r"ModuleNotFoundError: No module named '([^']+)'"
)

# R package names that are never valid Python packages. If the LLM generates
# `import withr` etc., attempting pip install is pointless and will crash.
# Starts with known R-only names; failed pip installs are added at runtime.
_SKIP_PACKAGES: set[str] = {
    "withr", "dplyr", "ggplot2", "magrittr", "tidyr", "purrr",
    "rlang", "tibble", "stringr", "forcats", "readr", "lubridate",
    "broom", "tidyverse", "devtools", "testthat", "usethis",
    "data.table", "caret", "mlr", "mlr3", "glue",
    "bsicons",
}


def _missing_module(stderr: str) -> str | None:
    """Return the top-level package name from a ModuleNotFoundError, or None."""
    m = _MISSING_MODULE_RE.search(stderr)
    if not m:
        return None
    # 'scipy.stats' → 'scipy'
    return m.group(1).split(".")[0]


def _auto_install_py(pkg: str) -> None:
    if pkg in _SKIP_PACKAGES:
        print(f"[r2py] Skipping install of '{pkg}' (known unavailable)")
        return
    from ..env.package_installer import install
    print(f"[r2py] Installing Python package '{pkg}' ...")
    try:
        install(py_packages=[pkg])
    except Exception as exc:
        _SKIP_PACKAGES.add(pkg)
        print(f"[r2py] Warning: failed to install '{pkg}': {exc}")


class PySandbox:
    """Run Python scripts in an isolated subprocess, capturing requested effects."""

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
        sidecar_files: dict[str, str] | None = None,
    ) -> EffectBundle:
        python = find_python()

        pre_parts: list[str] = []
        epi_parts: list[str] = []

        if EffectClass.GRAPHICS in capture:
            pre_parts.append(_graphics_effects.PY_PREAMBLE)
            epi_parts.append(_graphics_effects.PY_EPILOGUE)

        if EffectClass.ENV in capture:
            pre_parts.append(_env_effects.PY_PREAMBLE)
            epi_parts.append(_env_effects.PY_EPILOGUE)

        if EffectClass.WARNINGS in capture:
            pre_parts.append(_warnings_effects.PY_PREAMBLE)
            epi_parts.append(_warnings_effects.PY_EPILOGUE)

        if EffectClass.RNG in capture:
            pre_parts.append(_rng_effects.py_preamble(seed=seed, replay=replay))
            epi_parts.append(_rng_effects.PY_EPILOGUE_CAPTURE)
        elif seed is not None:
            pre_parts.append(
                f"import random as _r2py_seed_mod; _r2py_seed_mod.seed({seed})\n"
                f"try:\n    import numpy as _np_seed; _np_seed.random.seed({seed})\nexcept ImportError:\n    pass\n"
            )

        if EffectClass.DATA in capture:
            pre_parts.append(_data_effects.build_py_preamble())
            epi_parts.append(_data_effects.PY_EPILOGUE_TEMPLATE)

        if EffectClass.NETWORK in capture:
            pre_parts.append(_network_effects.PY_PREAMBLE)
            epi_parts.append(_network_effects.PY_EPILOGUE)

        if EffectClass.HTML in capture:
            epi_parts.append(_html_effects.PY_EPILOGUE)

        before_files = _files_effects.snapshot(workdir) if EffectClass.FILES in capture else {}
        home_snap = snapshot_home()

        before_source = "\n".join(pre_parts) + "\n" + preamble + "\n"
        _preamble_lines = before_source.count("\n")

        full_script = (
            before_source
            + source
            + "\n"
            + epilogue
            + "\n"
            + "\n".join(epi_parts)
        )

        script_path = workdir / "_r2py_script.py"
        script_path.write_text(full_script, encoding="utf-8")

        # Stage sidecar files (data-loading shim payload, etc.) next to the
        # script so its ``Path(__file__).parent / "<name>"`` lookup resolves.
        if sidecar_files:
            for fn, content in sidecar_files.items():
                (workdir / fn).write_text(content, encoding="utf-8")

        t_start = time.monotonic()
        try:
            result = subprocess.run(
                [str(python), str(script_path)],
                cwd=str(workdir),
                capture_output=True,
                timeout=timeout_s,
                env=scrub_env(),
            )
        except subprocess.TimeoutExpired:
            return EffectBundle(
                exit_code=1,
                stderr=f"TimeoutExpired: script exceeded {timeout_s}s sandbox limit",
                preamble_lines=_preamble_lines,
            )
        run_time = time.monotonic() - t_start

        if result.returncode != 0:
            stderr_text = result.stderr.decode("utf-8", errors="replace")
            pkg = _missing_module(stderr_text)
            if pkg:
                _auto_install_py(pkg)
                t_retry = time.monotonic()
                try:
                    result = subprocess.run(
                        [str(python), str(script_path)],
                        cwd=str(workdir),
                        capture_output=True,
                        timeout=timeout_s,
                        env=scrub_env(),
                    )
                except subprocess.TimeoutExpired:
                    return EffectBundle(
                        exit_code=1,
                        stderr=f"TimeoutExpired: script exceeded {timeout_s}s sandbox limit (after module install)",
                        preamble_lines=_preamble_lines,
                    )
                run_time += time.monotonic() - t_retry

        check_escape(home_snap, workdir)

        bundle = EffectBundle(exit_code=result.returncode, run_time_s=run_time, preamble_lines=_preamble_lines)

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

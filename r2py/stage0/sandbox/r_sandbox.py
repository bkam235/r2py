"""Rscript subprocess sandbox (§2.3)."""
from __future__ import annotations

import os
import re
import subprocess
import sys
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
from ..env.r_runtime import find_r, find_rscript, _R_ENV_DIR
from .base import ReplayLog, SandboxEscape
from .isolation import TempWorkdir, check_escape, scrub_env, snapshot_home

# Project library — the only library the R sandbox is allowed to use.
_R_PROJECT_LIB = _R_ENV_DIR / "library"

# R code prepended to every script to lock down the library search path,
# enable rlang::is_interactive() so examplesIf-guarded code executes,
# and prevent shinyApp() auto-print from blocking on runApp().
_LIBPATH_PREAMBLE = (
    f'.libPaths(c({repr(str(_R_PROJECT_LIB).replace(chr(92), "/"))}))\n'
    'options(rlang_interactive = TRUE)\n'
    'setHook(packageEvent("shiny", "onLoad"), function(...) {\n'
    '  assignInNamespace("print.shiny.appobj",\n'
    '    function(x, ...) invisible(x), ns = "shiny")\n'
    '})\n'
)

# Matches R's "no package" error in English and German locales.
_MISSING_PKG_RE = re.compile(
    r"(?:there is no package called|es gibt kein Paket namens)\s+['\"]([^'\"]+)['\"]",
    re.IGNORECASE,
)


def _missing_package(stderr: str) -> str | None:
    """Return the first missing R package name found in stderr, or None."""
    m = _MISSING_PKG_RE.search(stderr)
    return m.group(1) if m else None


def _auto_install(pkg: str) -> None:
    """Ensure *pkg* is available in the project library.

    Tries renv::restore() first (covers all packages in renv.lock).
    Falls back to install.packages() for packages not in the lockfile.
    """
    from ..env.r_env_setup import restore_r_env, _LOCKFILE
    import json

    # Check if the package is listed in renv.lock.
    in_lockfile = False
    if _LOCKFILE.exists():
        try:
            lock = json.loads(_LOCKFILE.read_text(encoding="utf-8"))
            in_lockfile = pkg in lock.get("Packages", {})
        except Exception:
            pass

    if in_lockfile:
        restore_r_env()
    else:
        # Package not in lockfile — install directly from CRAN into project library.
        from ..env.package_installer import install
        print(f"[r2py] Installing R package '{pkg}' from CRAN ...")
        install(r_packages=[pkg])


def _run_with_tree_kill(
    cmd: list[str],
    cwd: str,
    env: dict,
    timeout_s: float,
) -> subprocess.CompletedProcess:
    """Run a subprocess, killing the entire process tree on timeout (Windows).

    On Windows, R.exe spawns Rterm.exe as a child.  subprocess.run's timeout
    only kills the top-level process, leaving Rterm alive and holding pipes
    open — which causes the caller to hang indefinitely.  This helper uses
    taskkill /T to tear down the whole tree.
    """
    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        **({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
           if sys.platform == "win32" else {}),
    )
    try:
        stdout, stderr = proc.communicate(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        if sys.platform == "win32":
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                capture_output=True,
            )
        else:
            proc.kill()
        stdout, stderr = proc.communicate(timeout=10)
        raise subprocess.TimeoutExpired(cmd, timeout_s, stdout, stderr)
    return subprocess.CompletedProcess(cmd, proc.returncode, stdout, stderr)


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
        r_exe = find_r()

        # Build capture preambles/epilogues in addition to caller-supplied ones.
        pre_parts: list[str] = []
        epi_parts: list[str] = []

        if seed is not None:
            pre_parts.append(f"set.seed({seed}L)\n")

        # Preambles: ENV before WARNINGS so ENV captures baseline options before
        # warning.expression is installed.  Epilogues: WARNINGS before ENV so
        # warning.expression is restored before the options diff is taken.

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

        # ENV preamble before WARNINGS preamble (captures baseline before warning.expression is set)
        if EffectClass.ENV in capture:
            pre_parts.append(_env_effects.R_PREAMBLE)

        if EffectClass.WARNINGS in capture:
            pre_parts.append(_warnings_effects.R_PREAMBLE_SIMPLE)

        if EffectClass.RNG in capture:
            pre_parts.append(_rng_effects.r_preamble(seed=seed, replay=replay))
            epi_parts.append(_rng_effects.R_EPILOGUE_CAPTURE)

        if EffectClass.NETWORK in capture:
            pre_parts.append(_network_effects.R_PREAMBLE)
            epi_parts.append(_network_effects.R_EPILOGUE)

        # WARNINGS epilogue before ENV epilogue (restores warning.expression before options diff)
        if EffectClass.WARNINGS in capture:
            epi_parts.append(_warnings_effects.R_EPILOGUE_SIMPLE)

        if EffectClass.ENV in capture:
            epi_parts.append(_env_effects.R_EPILOGUE)

        # FILES epilogue LAST — copies tempdir() contents into workdir before
        # R's session cleanup removes them.
        if EffectClass.FILES in capture:
            epi_parts.append(_files_effects.R_EPILOGUE_FILES)

        # Snapshot workdir before run (for files diff)
        before_files = _files_effects.snapshot(workdir) if EffectClass.FILES in capture else {}

        # Snapshot home for escape detection
        home_snap = snapshot_home()

        # Assemble the full script — library path lock comes first
        full_script = (
            _LIBPATH_PREAMBLE
            + "\n".join(pre_parts)
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

        # Redirect R's tempdir()/tempfile() into the sandbox workdir so that
        # files written via temp paths are captured by the FILES snapshot.
        run_env = scrub_env()
        run_env["TMPDIR"] = str(workdir)

        script_path_r = str(script_path).replace("\\", "/")
        r_cmd = [str(r_exe), "--vanilla", "--quiet", "-e",
                 f'source("{script_path_r}", print.eval=TRUE)']
        t_start = time.monotonic()
        result = _run_with_tree_kill(r_cmd, cwd=str(workdir),
                                     env=run_env, timeout_s=timeout_s)
        run_time = time.monotonic() - t_start

        # Escape detection
        check_escape(home_snap, workdir)

        if result.returncode != 0:
            stderr_text = result.stderr.decode("utf-8", errors="replace")
            pkg = _missing_package(stderr_text)
            if pkg:
                # Auto-install the missing package and retry once.
                _auto_install(pkg)
                result = _run_with_tree_kill(r_cmd, cwd=str(workdir),
                                             env=run_env, timeout_s=timeout_s)

        # Raise on any remaining non-zero exit (including after retry).
        if result.returncode != 0:
            stderr_tail = result.stderr.decode("utf-8", errors="replace").strip()
            if len(stderr_tail) > 600:
                stderr_tail = "..." + stderr_tail[-600:]
            raise RuntimeError(
                f"R script exited with code {result.returncode}:\n{stderr_tail}"
            )

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

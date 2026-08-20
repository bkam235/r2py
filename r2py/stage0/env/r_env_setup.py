"""Restore the project-local R virtual environment from renv.lock (§2.4).

Usage:
    from r2py.stage0.env.r_env_setup import restore_r_env
    restore_r_env()          # uses the bundled r_env by default
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from .r_runtime import find_rscript, _R_ENV_DIR

_LIBRARY = _R_ENV_DIR / "library"
_LOCKFILE = _R_ENV_DIR / "renv.lock"


def _clean_env() -> dict[str, str]:
    """Minimal environment for R install subprocess: no stray lib-path overrides."""
    env = dict(os.environ)
    env["LANGUAGE"] = "en"
    for var in ("R_LIBS", "R_LIBS_USER", "R_LIBS_SITE"):
        env.pop(var, None)
    return env


def restore_r_env() -> None:
    """Install all packages listed in renv.lock into the project library.

    Idempotent: already-installed packages are skipped by renv::restore.
    Raises RuntimeError if renv.lock is missing or the restore fails.
    """
    rscript = find_rscript()

    if not _LOCKFILE.exists():
        raise RuntimeError(
            f"renv.lock not found at {_LOCKFILE}. "
            "Cannot restore R packages."
        )

    lib_r = str(_LIBRARY).replace("\\", "/")
    lock_r = str(_LOCKFILE).replace("\\", "/")

    print(f"[r2py] Restoring R packages from {_LOCKFILE} ...")
    subprocess.run(
        [
            str(rscript), "-e",
            f".libPaths(c('{lib_r}')); "
            f"renv::restore(lockfile='{lock_r}', library='{lib_r}', prompt=FALSE)",
        ],
        check=True,
        env=_clean_env(),
    )
    print("[r2py] R package restore complete.")

"""Rscript discovery and R version detection (§2.4)."""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

# Bundled R environment shipped with r2py.
_R_ENV_DIR = Path(__file__).parent.parent / "r_env"


def find_rscript() -> Path:
    """Return the path to Rscript, raising RuntimeError if not found."""
    # 0. Bundled R environment (always preferred — ensures hermetic package set)
    bundled = _R_ENV_DIR / "runtime" / "bin" / "Rscript.exe"
    if bundled.exists():
        return bundled

    # 1. PATH lookup
    found = shutil.which("Rscript")
    if found:
        return Path(found)

    # 2. Windows common install locations
    import glob
    for pattern in [
        r"C:\Program Files\R\R-*\bin\Rscript.exe",
        r"C:\Program Files (x86)\R\R-*\bin\Rscript.exe",
    ]:
        matches = sorted(glob.glob(pattern), reverse=True)  # newest first
        if matches:
            return Path(matches[0])

    # 3. Unix common locations
    for candidate in [
        "/usr/bin/Rscript",
        "/usr/local/bin/Rscript",
        "/opt/homebrew/bin/Rscript",
        "/opt/local/bin/Rscript",
    ]:
        p = Path(candidate)
        if p.exists():
            return p

    raise RuntimeError(
        "Rscript not found. Install R and ensure Rscript is on PATH, "
        "or set R2PY_RSCRIPT env var to its full path."
    )


def find_r_library() -> "Path | None":
    """Return the bundled R library path, or None if not present.

    The bundled library ships at ``r_env/library/`` alongside the runtime.
    Callers use this to prepend the hermetic package set to ``.libPaths()``
    before running ad-hoc Rscript subprocesses.
    """
    lib = _R_ENV_DIR / "library"
    return lib if lib.is_dir() else None


def find_r() -> Path:
    """Return the path to R (not Rscript), raising RuntimeError if not found.

    R and Rscript are always co-installed in the same bin directory, so we
    locate Rscript first and swap the executable name.
    """
    rscript = find_rscript()
    suffix = rscript.suffix  # ".exe" on Windows, "" on Unix
    r_exe = rscript.parent / f"R{suffix}"
    if r_exe.exists():
        return r_exe
    raise RuntimeError(
        f"R executable not found next to Rscript at {rscript}. "
        "R and Rscript are always co-installed — this is unexpected."
    )


def r_version() -> str:
    """Return the R version string (e.g. '4.3.1'), raising RuntimeError on failure."""
    rscript = find_rscript()
    result = subprocess.run(
        [str(rscript), "--version"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=10,
    )
    # R prints version to stderr: "R scripting front-end version 4.3.1 (2023-06-16)"
    output = result.stdout + result.stderr
    m = re.search(r"\b(\d+\.\d+\.\d+)\b", output)
    if m:
        return m.group(1)
    raise RuntimeError(f"Could not parse R version from: {output!r}")

#!/usr/bin/env python3
"""Set up the R package library for r2py.

Requires R (>= 4.4) to be installed on your system.
Downloads and installs all R packages needed for execution-equivalence testing.

Usage:
    python scripts/setup_r_env.py
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
R_ENV = ROOT / "r2py" / "stage0" / "r_env"
LIBRARY = R_ENV / "library"
LOCKFILE = R_ENV / "renv.lock"
CRAN = "https://cloud.r-project.org"

# Packages to install beyond what renv.lock covers.
# The sandbox auto-installs missing packages at runtime,
# but pre-installing these avoids delays during translation.
EXTRA_PACKAGES = [
    "tidyverse",
    "shiny",
    "data.table",
    "caret",
    "lavaan",
    "knitr",
    "rmarkdown",
    "testthat",
    "xtable",
    "plyr",
    "reshape2",
    "magick",
    "clock",
    "glmnet",
    "ragg",
    "pkgdown",
    "prodlim",
    "progressr",
    "bit64",
]


def find_rscript() -> Path | None:
    """Find Rscript on this system, matching r_runtime.py's fallback cascade."""
    bundled = R_ENV / "runtime" / "bin" / (
        "Rscript.exe" if sys.platform == "win32" else "Rscript"
    )
    if bundled.exists():
        return bundled

    which = shutil.which("Rscript")
    if which:
        return Path(which)

    if sys.platform == "win32":
        import glob
        for pattern in [
            r"C:\Program Files\R\R-*\bin\Rscript.exe",
            r"C:\Program Files (x86)\R\R-*\bin\Rscript.exe",
        ]:
            hits = sorted(glob.glob(pattern), reverse=True)
            if hits:
                return Path(hits[0])

    for p in ("/usr/bin/Rscript", "/usr/local/bin/Rscript",
              "/opt/homebrew/bin/Rscript", "/opt/local/bin/Rscript"):
        if Path(p).exists():
            return Path(p)

    return None


def _clean_env() -> dict[str, str]:
    env = dict(os.environ)
    env["LANGUAGE"] = "en"
    for var in ("R_LIBS", "R_LIBS_USER", "R_LIBS_SITE"):
        env.pop(var, None)
    return env


def run_r(rscript: Path, code: str) -> None:
    subprocess.run([str(rscript), "-e", code], check=True, env=_clean_env())


def main() -> int:
    print("=== r2py R environment setup ===\n")

    rscript = find_rscript()
    if rscript is None:
        print("ERROR: Rscript not found.")
        print("Install R (>= 4.4) from https://cloud.r-project.org")
        return 1

    result = subprocess.run(
        [str(rscript), "--version"], capture_output=True, text=True,
    )
    version_line = (result.stderr or result.stdout).strip().splitlines()[0]
    print(f"Rscript:  {rscript}")
    print(f"Version:  {version_line}")

    LIBRARY.mkdir(parents=True, exist_ok=True)
    lib_r = str(LIBRARY).replace("\\", "/")
    print(f"Library:  {LIBRARY}\n")

    # Step 1: bootstrap renv
    print("[1/3] Installing renv ...")
    run_r(rscript,
          f"install.packages('renv', lib='{lib_r}', "
          f"repos='{CRAN}', quiet=TRUE)")

    # Step 2: restore pinned packages from lockfile
    if LOCKFILE.exists():
        print("[2/3] Restoring packages from renv.lock ...")
        lock_r = str(LOCKFILE).replace("\\", "/")
        run_r(rscript,
              f".libPaths(c('{lib_r}')); "
              f"renv::restore(lockfile='{lock_r}', library='{lib_r}', "
              f"prompt=FALSE)")
    else:
        print("[2/3] No renv.lock found — skipping restore.")

    # Step 3: install additional packages (tidyverse, shiny, etc.)
    print("[3/3] Installing additional packages ...")
    pkg_vec = ", ".join(f"'{p}'" for p in EXTRA_PACKAGES)
    run_r(rscript,
          f".libPaths(c('{lib_r}')); "
          f"install.packages(c({pkg_vec}), lib='{lib_r}', "
          f"repos='{CRAN}', dependencies=TRUE, quiet=TRUE)")

    installed = [d.name for d in LIBRARY.iterdir() if d.is_dir()]
    print(f"\n=== Setup complete — {len(installed)} packages installed ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())

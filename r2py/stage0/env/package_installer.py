"""Idempotent R/Python package installation with lockfile (§2.4)."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from .r_runtime import find_rscript, _R_ENV_DIR
from .py_runtime import find_python
from .r_env_setup import _clean_env

_R_PROJECT_LIB = _R_ENV_DIR / "library"

# Valid R/Python package name: starts with a letter, then letters/digits/._-
_PKG_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9._-]*$")


def _validate_package_name(name: str) -> None:
    """Raise ValueError if *name* is not a safe package identifier."""
    if not _PKG_NAME_RE.match(name):
        raise ValueError(
            f"Invalid package name {name!r}: must match ^[A-Za-z][A-Za-z0-9._-]*$"
        )

_DEFAULT_LOCKFILE = Path("work/lock.json")


def _read_lock(lockfile: Path) -> dict:
    if lockfile.exists():
        try:
            return json.loads(lockfile.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _write_lock(lock: dict, lockfile: Path) -> None:
    lockfile.parent.mkdir(parents=True, exist_ok=True)
    lockfile.write_text(json.dumps(lock, indent=2), encoding="utf-8")


def get_r_package_version(package: str) -> str | None:
    """Return the installed version of an R package, or None if not installed."""
    rscript = find_rscript()
    result = subprocess.run(
        [str(rscript), "-e",
         f"cat(tryCatch(as.character(packageVersion('{package}')), error=function(e) 'NOT_INSTALLED'))"],
        capture_output=True, text=True, encoding="utf-8", timeout=15,
    )
    v = result.stdout.strip()
    return None if v == "NOT_INSTALLED" or not v else v


def get_py_package_version(package: str) -> str | None:
    """Return the installed version of a Python package, or None if not installed."""
    python = find_python()
    result = subprocess.run(
        [str(python), "-c",
         f"import importlib.metadata; print(importlib.metadata.version('{package}'))"],
        capture_output=True, text=True, encoding="utf-8", timeout=10,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def install(
    r_packages: list[str] = (),
    py_packages: list[str] = (),
    lockfile: Path = _DEFAULT_LOCKFILE,
) -> None:
    """Install R and Python packages idempotently, updating the lockfile.

    Already-locked packages are skipped.  New installs are recorded with their
    version.  Bioconductor packages can be prefixed with 'bioc::' (e.g.
    'bioc::DESeq2').
    """
    lock = _read_lock(lockfile)
    r_lock: dict = lock.setdefault("r", {})
    py_lock: dict = lock.setdefault("py", {})

    rscript = find_rscript()
    lib_r = str(_R_PROJECT_LIB).replace("\\", "/")

    for pkg in r_packages:
        if pkg in r_lock:
            continue
        bioc = pkg.startswith("bioc::")
        bare = pkg[len("bioc::"):] if bioc else pkg
        _validate_package_name(bare)
        if bioc:
            cmd = (
                f".libPaths(c('{lib_r}')); "
                f"if (!requireNamespace('BiocManager', quietly=TRUE)) "
                f"install.packages('BiocManager', lib='{lib_r}', repos='https://cloud.r-project.org'); "
                f"BiocManager::install('{bare}', lib='{lib_r}', ask=FALSE)"
            )
        else:
            cmd = (
                f".libPaths(c('{lib_r}')); "
                f"install.packages('{bare}', lib='{lib_r}', repos='https://cloud.r-project.org')"
            )
        subprocess.run(
            [str(rscript), "-e", cmd],
            check=True, timeout=300,
            env=_clean_env(),
        )
        version = get_r_package_version(bare) or "unknown"
        r_lock[pkg] = version

    python = find_python()

    for pkg in py_packages:
        if pkg in py_lock:
            continue
        # Strip version specifiers before validating the bare name
        bare_py = re.split(r"[><=!;]", pkg)[0].strip()
        _validate_package_name(bare_py)
        subprocess.run(
            [str(python), "-m", "pip", "install", pkg],
            check=True, timeout=300,
        )
        version = get_py_package_version(bare_py) or "unknown"
        py_lock[pkg] = version

    _write_lock(lock, lockfile)

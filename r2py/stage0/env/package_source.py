"""Locate installed R/Python package source directories (§2.4)."""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

from .r_runtime import find_rscript, find_r_library


def find_r_package_source(package: str) -> Path | None:
    """Return the path to the installed R package directory, or None."""
    rscript = find_rscript()
    lib = find_r_library()
    lib_setup = (
        f".libPaths(c('{lib.as_posix()}', .libPaths())); "
        if lib else ""
    )
    result = subprocess.run(
        [str(rscript), "-e",
         f"{lib_setup}cat(tryCatch(find.package('{package}'), error=function(e) ''))"],
        capture_output=True, text=True, encoding="utf-8", timeout=10,
    )
    path_str = result.stdout.strip()
    if path_str:
        p = Path(path_str)
        if p.exists():
            return p
    return None


def find_py_package_source(package: str) -> Path | None:
    """Return the path to the installed Python package source directory, or None."""
    spec = importlib.util.find_spec(package)
    if spec is None:
        return None
    # Prefer submodule_search_locations (package directory) over origin (single file)
    if spec.submodule_search_locations:
        locations = list(spec.submodule_search_locations)
        if locations:
            return Path(locations[0])
    if spec.origin:
        return Path(spec.origin).parent
    return None

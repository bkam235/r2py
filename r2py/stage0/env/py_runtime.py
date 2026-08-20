"""Python interpreter discovery (§2.4)."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def find_python() -> Path:
    """Return the path to a Python ≥3.11 interpreter.

    Checks R2PY_PYTHON env var first, then falls back to sys.executable (the
    interpreter that is currently running r2py).
    """
    override = os.environ.get("R2PY_PYTHON")
    if override:
        p = Path(override)
        if not p.exists():
            raise RuntimeError(f"R2PY_PYTHON points to a non-existent path: {p}")
        return p
    return Path(sys.executable)


def python_version() -> str:
    """Return the Python version string (e.g. '3.11.4')."""
    v = sys.version_info
    return f"{v.major}.{v.minor}.{v.micro}"

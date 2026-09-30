"""Python interpreter discovery (§2.4)."""
from __future__ import annotations

import functools
import json
import os
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]


def _project_sandbox_python() -> Path | None:
    """``.venv-sandbox`` in the project root, if present: a dedicated interpreter for running
    translations, newer than the harness's own (3.12+ lifts the 3.10 f-string limits the model
    keeps hitting) and independent of it."""
    for rel in ("Scripts/python.exe", "bin/python"):
        p = _ROOT / ".venv-sandbox" / rel
        if p.exists():
            return p
    return None


def find_python() -> Path:
    """Return the interpreter that runs translated code.

    ``R2PY_PYTHON`` first, then the project's ``.venv-sandbox``, then ``sys.executable``.
    """
    override = os.environ.get("R2PY_PYTHON")
    if override:
        p = Path(override)
        if not p.exists():
            raise RuntimeError(f"R2PY_PYTHON points to a non-existent path: {p}")
        return p
    return _project_sandbox_python() or Path(sys.executable)


def python_version() -> str:
    """Return the version string (e.g. '3.13.9') of the interpreter that runs translations."""
    return ".".join(str(x) for x in sandbox_version_info()[:3])


@functools.lru_cache(maxsize=None)
def _version_of(python: str) -> tuple[int, int, int]:
    if Path(python) == Path(sys.executable):
        return tuple(sys.version_info[:3])  # type: ignore[return-value]
    out = subprocess.run([python, "-c", "import sys;print(*sys.version_info[:3])"],
                         capture_output=True, text=True, timeout=30).stdout.split()
    return tuple(int(x) for x in out)  # type: ignore[return-value]


def sandbox_version_info() -> tuple[int, int, int]:
    return _version_of(str(find_python()))


_PARSE = """
import ast, json, sys
src = sys.stdin.read()
try:
    ast.parse(src)
except SyntaxError as e:
    print(json.dumps({"lineno": e.lineno, "msg": e.msg, "text": e.text, "offset": e.offset}))
"""


def syntax_error_in_sandbox_python(source: str) -> dict | None:
    """Parse ``source`` with the interpreter that will run it: the harness's own may be older, and
    would reject valid newer syntax (nested f-string quotes).  None means it parses."""
    python = find_python()
    if Path(python) == Path(sys.executable):
        import ast
        try:
            ast.parse(source)
        except SyntaxError as e:
            return {"lineno": e.lineno, "msg": e.msg, "text": e.text, "offset": e.offset}
        return None
    r = subprocess.run([str(python), "-c", _PARSE], input=source, capture_output=True, text=True,
                       timeout=30, encoding="utf-8")
    return json.loads(r.stdout) if r.stdout.strip() else None

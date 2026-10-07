"""Predict ``ModuleNotFoundError`` before a translation is run.

The sandbox handles a missing module by ``pip install``-ing it; when that fails the script
crashes.  A rewrite that imports an R package name (``import magrittr``, ``import openssl``) then
costs a whole verification to learn what could have been known up front.  ``unavailable_imports``
returns the modules a script imports that are neither importable by the interpreter that runs
translations nor installable from PyPI, so the agent can be told before spending a step.

Whether a name is on PyPI is looked up with ``pip index versions`` and cached in
``work/pypi_names.json`` (shared by parallel workers; a race only repeats a lookup).
"""
from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path

from .py_runtime import find_python

_CACHE = Path(__file__).resolve().parents[3] / "work" / "pypi_names.json"
_PROBE = """
import importlib.util, json, sys
names = json.loads(sys.stdin.read())
def ok(n):
    try:
        return importlib.util.find_spec(n) is not None
    except Exception:
        return True   # a broken parent package still means the name exists
print(json.dumps([n for n in names if not ok(n)]))
"""


_NAMES_PROBE = """
import importlib, importlib.util, json, sys
pairs = json.loads(sys.stdin.read())          # [[module, name], ...]
bad = []
for mod, name in pairs:
    try:
        m = importlib.import_module(mod)
    except Exception:
        continue                                # a module that cannot be imported is the other check's business
    if hasattr(m, name):
        continue
    try:
        if importlib.util.find_spec(mod + "." + name) is not None:
            continue                            # a submodule
    except ModuleNotFoundError:
        pass                                    # e.g. "'os' is not a package": there is no such submodule
    except Exception:
        continue
    import difflib
    pub = [n for n in dir(m) if not n.startswith("_")]
    near = difflib.get_close_matches(name, pub, n=3, cutoff=0.6)
    if not near and hasattr(m, "__path__"):
        # Not in the package namespace: a close name in one of its submodules (pygments.lexers.r.SLexer)
        import pkgutil, time
        t0 = time.monotonic()
        scored = []
        for info in list(pkgutil.iter_modules(m.__path__))[:500]:
            if time.monotonic() - t0 > 12:
                break
            try:
                sub = importlib.import_module(mod + "." + info.name)
            except Exception:
                continue
            for hit in difflib.get_close_matches(name, [n for n in dir(sub) if not n.startswith("_")], n=2, cutoff=0.8):
                scored.append((difflib.SequenceMatcher(None, name, hit).ratio(), mod + "." + info.name + "." + hit))
        near = [n for _r, n in sorted(scored, reverse=True)[:6]]
    bad.append([mod, name, near[:6]])
print(json.dumps(bad))
"""


def imported_names(source: str) -> list[tuple[str, str]]:
    """``(module, name)`` for every ``from module import name`` (absolute, named, not star)."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module and node.module != "__future__":
            out += [(node.module, a.name) for a in node.names if a.name != "*"]
    return out


_NAMES_CACHE: dict[tuple[str, str], list | None] = {}


def missing_import_names(source: str) -> list[tuple[str, str, list[str]]]:
    """``from module import name`` where *module* imports but has no such name: ``(module, name, near spellings)``.

    A model writes ``from pygments.lexers import RLexer`` or ``from shiny import http_response``; both modules are
    installed, the names do not exist, and the script dies at its first line.  The check runs in the interpreter that
    runs translations, once per (module, name), so it adds a second or two the first time and nothing after.
    """
    pairs = [p for p in dict.fromkeys(imported_names(source)) if p not in _NAMES_CACHE]
    if pairs:
        try:
            r = subprocess.run([str(find_python()), "-c", _NAMES_PROBE], input=json.dumps(pairs), capture_output=True,
                               text=True, timeout=90, encoding="utf-8")
            bad = {(m, n): near for m, n, near in json.loads(r.stdout)}
        except (subprocess.TimeoutExpired, OSError, ValueError):
            return []                           # cannot tell: do not block
        for p in pairs:
            _NAMES_CACHE[p] = bad.get(p)
    return [(m, n, _NAMES_CACHE[(m, n)]) for m, n in dict.fromkeys(imported_names(source)) if _NAMES_CACHE.get((m, n)) is not None]


def imported_modules(source: str) -> set[str]:
    """Top-level names a script imports (absolute imports only)."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module.split(".")[0])
    names.discard("__future__")
    return names


def _not_importable(names: list[str]) -> list[str]:
    if not names:
        return []
    r = subprocess.run([str(find_python()), "-c", _PROBE], input=json.dumps(sorted(names)),
                       capture_output=True, text=True, timeout=60, encoding="utf-8")
    try:
        return json.loads(r.stdout)
    except ValueError:
        return []  # cannot tell: do not block


def _load_cache() -> dict[str, bool]:
    try:
        return json.loads(_CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _on_pypi(name: str) -> bool | None:
    """True/False from ``pip index versions``; None when it could not be determined."""
    cache = _load_cache()
    if name in cache:
        return cache[name]
    try:
        r = subprocess.run([str(find_python()), "-m", "pip", "index", "versions", name],
                           capture_output=True, text=True, timeout=30)
    except (subprocess.TimeoutExpired, OSError):
        return None
    out = (r.stdout + r.stderr).lower()
    if r.returncode == 0:
        found = True
    elif "no matching distribution" in out or "could not find a version" in out:
        found = False
    else:
        return None  # offline, rate-limited, ...: not evidence either way
    cache[name] = found
    try:
        _CACHE.parent.mkdir(parents=True, exist_ok=True)
        _CACHE.write_text(json.dumps(cache, indent=1), encoding="utf-8")
    except OSError:
        pass
    return found


def unavailable_imports(source: str, known_unavailable: frozenset[str] | set[str] = frozenset()) -> list[str]:
    """Modules ``source`` imports that would fail at run time even after the sandbox's auto-install."""
    missing = _not_importable(sorted(imported_modules(source)))
    return [m for m in missing if m in known_unavailable or _on_pypi(m) is False]

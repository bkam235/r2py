"""Workdir file snapshot and diff (§2.2)."""
from __future__ import annotations

import hashlib
from pathlib import Path


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot(workdir: Path) -> dict[str, str]:
    """Return {relative_path: sha256_hex} for every file under workdir."""
    result: dict[str, str] = {}
    for p in workdir.rglob("*"):
        if p.is_file():
            rel = str(p.relative_to(workdir))
            try:
                result[rel] = _sha256(p)
            except OSError:
                pass
    return result


def diff(before: dict[str, str], after: dict[str, str]) -> dict[str, str]:
    """Return entries present or changed in *after* relative to *before*.

    Keys that existed before with the same hash are omitted (unchanged).
    Deleted files are not reported — callers that need deletions can compare
    key sets themselves.
    """
    return {
        path: hash_
        for path, hash_ in after.items()
        if before.get(path) != hash_
    }


def collect(workdir: Path, before: dict[str, str]) -> dict:
    """Take an after-snapshot of workdir and return EffectBundle.files diff."""
    after = snapshot(workdir)
    changed = diff(before, after)
    # Exclude internal r2py capture files
    changed = {k: v for k, v in changed.items() if not k.startswith("_r2py_")}
    return {"files": changed}

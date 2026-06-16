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
    # Exclude internal r2py capture files and the tempdir preserve directory
    changed = {k: v for k, v in changed.items() if not k.startswith("_r2py_")}
    # Include files preserved from R's tempdir (copied by R_EPILOGUE_FILES
    # before R cleans up).  Report them under a flat "tempfile:<basename>" key
    # so the comparator sees them as semantically meaningful file writes.
    preserve_dir = workdir / "_r2py_tempfiles"
    if preserve_dir.is_dir():
        for p in preserve_dir.rglob("*"):
            if p.is_file():
                try:
                    key = "tempfile:" + p.name
                    changed[key] = _sha256(p)
                except OSError:
                    pass
    return {"files": changed}


# R epilogue that copies user-created files from tempdir() into the workdir
# before R's session cleanup removes them.  Only copies files the script
# created (not R's internal session files like .RData, .Rhistory, etc.).
R_EPILOGUE_FILES = r"""
tryCatch({
  .r2py_td <- tempdir()
  .r2py_preserve <- file.path(getwd(), "_r2py_tempfiles")
  dir.create(.r2py_preserve, showWarnings = FALSE, recursive = TRUE)
  .r2py_tf <- list.files(.r2py_td, full.names = TRUE, recursive = TRUE)
  # Skip R internal files and r2py capture files.
  .r2py_skip <- c(".RData", ".Rhistory", ".Rprofile", "Rplots.pdf")
  for (.r2py_f in .r2py_tf) {
    .r2py_bn <- basename(.r2py_f)
    if (!.r2py_bn %in% .r2py_skip && !startsWith(.r2py_bn, "_r2py_")) {
      tryCatch(
        file.copy(.r2py_f, file.path(.r2py_preserve, .r2py_bn), overwrite = TRUE),
        error = function(e) NULL
      )
    }
  }
}, error = function(e) NULL)
"""

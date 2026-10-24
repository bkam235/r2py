"""Scoring version: which scorer produced a score (2026-10-24).

Scores are comparable only within a scoring epoch: the same scorer code and the same stored R ground truth. Three
verifier changes in October made earlier scores incomparable, and each time that was noticed by hand. This module
fingerprints the scorer so every run can record which epoch it was scored in, and so a change can trigger the
regression check (`scripts/scoring_epoch.py`).

The scorer is declared, not derived: importing the verifier also imports the agent through package imports, and a
prompt change must not open a new epoch. Agent code (prompts, the loop, the review) is outside it.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Code that turns a Python program and an R ground truth into a score.
SCORER_PATHS = (
    "r2py/stage0/effects",          # effect capture, R and Python sides
    "r2py/stage0/sandbox",          # how both programs are run
    "r2py/stage4",                  # verifier, decomposition, comparators
    "r2py/stage1/runner.py",        # R checkpointed capture (per-entity ground truth)
    "r2py/stage2/stitch.py",        # data shim build, activation, refresh
    "r2py/stage2/sentinel_mapper.py",   # entity attribution (sentinels, restoration, model mapping)
    "r2py/harness/tools.py",        # HarnessTools.verify: which attribution path is used
    "r2py/harness/objective.py",    # entity score, search key
    "r2py/types.py",
)
# The part of it that produces the stored R ground truth: a change here means the stored script maps must be
# re-captured (scripts/refresh_entity_bundles.py), not only re-scored.
R_CAPTURE_PATHS = ("r2py/stage1/runner.py", "r2py/stage0/effects", "r2py/stage0/sandbox/r_sandbox.py")


def _files(paths) -> list[Path]:
    out = []
    for rel in paths:
        p = ROOT / rel
        out += sorted(p.rglob("*.py")) if p.is_dir() else [p]
    return sorted(set(out))


def _hash(files) -> str:
    h = hashlib.sha256()
    for p in files:
        h.update(p.relative_to(ROOT).as_posix().encode())
        h.update(p.read_bytes().replace(b"\r\n", b"\n"))   # the same value on a Windows checkout and in git
    return h.hexdigest()[:12]


def scorer_hash() -> str:
    return _hash(_files(SCORER_PATHS))


def r_capture_hash() -> str:
    return _hash(_files(R_CAPTURE_PATHS))


def maps_hash(map_dir: Path | str = ROOT / "work/reverify/script_maps") -> str:
    """The stored R ground truth: every script map the training pool is scored against."""
    return _hash(sorted(Path(map_dir).glob("*.pkl")))


def scoring_version() -> str:
    """`<scorer code>-<stored R ground truth>`, recorded with every scored run."""
    return f"{scorer_hash()}-{maps_hash()}"

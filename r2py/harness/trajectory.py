"""Per-run trajectory log: one JSON line per event, so a run can be replayed and compared (Stage 9a).

Until now a run left only aggregates, and the first training run's per-step record was lost with
its stdout.  A trajectory has everything a later analysis needs to rebuild a state: the seeds with
their sources and scores, every agent step with its action, candidate source, outcome and per-entity
scores, and the final result.  Nothing here changes behaviour; with no ``begin()`` every call is a no-op.

Events (``kind``): ``run_start``, ``seed``, ``step`` (one per outcome of an agent step), ``accepted``,
``run_end``.  Each line also carries ``t`` (seconds since ``run_start``).
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

_state: dict | None = None


def begin(path: str | Path, **meta) -> None:
    """Start logging to ``path`` (appended to; one run per file is the convention)."""
    global _state
    end_run = _state
    if end_run is not None:
        end()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    _state = {"f": path.open("a", encoding="utf-8", buffering=1), "t0": time.monotonic(), "path": path}
    log("run_start", **meta)


def active() -> bool:
    return _state is not None


def log(kind: str, **fields) -> None:
    if _state is None:
        return
    rec = {"kind": kind, "t": round(time.monotonic() - _state["t0"], 2), **fields}
    _state["f"].write(json.dumps(rec, default=str) + "\n")


def end(**fields) -> None:
    global _state
    if _state is None:
        return
    log("run_end", **fields)
    _state["f"].close()
    _state = None


def source_hash(source: str) -> str:
    return hashlib.sha1(source.encode("utf-8")).hexdigest()[:12]


def read(path: str | Path) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]

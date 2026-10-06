"""Fixes the agent found, as candidates for the verified runtime (roadmap step 8).

The agent loop searches: some rewrite lifts an entity from a poor score to a good one.  That is evidence of how one R call
should be translated, found at the cost of model calls, in one script, and then it is gone.  Here every such fix is read off
the trajectory logs -- the entity whose score rose across two consecutive accepted sources, the R call that keys it, the
Python fragment before and after -- and becomes a candidate: the runtime pipeline (``propose.attempt``) is shown the fixed
fragment as evidence, asked for a general ``r_<name>``, and accepts it only if it reproduces R on the differential tests.
Search finds, the runtime generalises and verifies, and the knowledge is reusable by every later script.
"""
from __future__ import annotations

import glob
import json
import pickle
from dataclasses import dataclass
from pathlib import Path

from ..harness import objective  # noqa: F401  (documented dependency: entity scores are the verifier's)
from ..stage2.sentinel_mapper import ranges_from_sentinels

GOOD = 0.9          # an entity at or above this is correct
POOR = 0.7          # a fix lifts an entity from below this
MAX_FRAGMENT = 40   # lines


@dataclass
class Fix:
    script: str
    eid: str
    package: str
    function: str
    r_text: str                 # the entity's R source
    span: tuple[int, int]       # its 0-based inclusive line span in the script
    before: str                 # the Python fragment of the entity before the rewrite
    after: str                  # ... and after
    score_before: float
    score_after: float
    r_source: str = ""          # the whole script (for mining cases)


def _fragment(source: str, eid: str) -> str:
    ranges = ranges_from_sentinels(source).get(eid)
    if not ranges:
        return ""
    lines = [l for l in source.splitlines() if not l.lstrip().startswith("# r2py:entity:")]
    return "\n".join("\n".join(lines[s - 1:e]) for s, e in ranges)[:4000]


def fixes_from_trajectories(trajectory_files: list[str], script_map_dir: str | Path) -> list[Fix]:
    """Entities lifted from < POOR to >= GOOD between two consecutive accepted sources of a run."""
    from ..harness import trajectory
    from ..library.pattern import pattern_key

    out: list[Fix] = []
    for f in trajectory_files:
        recs = trajectory.read(f)
        if not recs:
            continue
        script = recs[0].get("script", "")
        pkl = Path(script_map_dir) / (Path(script).stem + ".pkl")
        if not pkl.exists():
            continue
        sm = pickle.loads(pkl.read_bytes())
        states = [r for r in recs if r["kind"] == "accepted" and r.get("per_entity") and r.get("source")]
        for prev, cur in zip(states, states[1:]):
            for eid, after in cur["per_entity"].items():
                before = prev["per_entity"].get(eid)
                ent = sm.entities.get(eid)
                span = getattr(ent, "source_span", None)
                if before is None or ent is None or span is None or not (before < POOR and after >= GOOD):
                    continue
                key = pattern_key(ent)
                if not key:
                    continue
                lines = (sm.source or "").splitlines()
                out.append(Fix(script, eid, key[0], key[1], "\n".join(lines[span.start_line:span.end_line + 1]),
                               (span.start_line, span.end_line), _fragment(prev["source"], eid), _fragment(cur["source"], eid),
                               round(before, 3), round(after, 3), sm.source or ""))
    return out


def candidates(fixes: list[Fix], known: set[str]) -> dict[str, list[Fix]]:
    """Fixes grouped by R function, dropping functions the store already has and fragments too long to read."""
    by: dict[str, list[Fix]] = {}
    for fx in fixes:
        if fx.function in known or fx.after.count("\n") > MAX_FRAGMENT or not fx.after.strip():
            continue
        by.setdefault(fx.function, []).append(fx)
    return by


def hint(fx: Fix) -> str:
    """What the model is shown: evidence from a real script, not a specification."""
    text = (f"Evidence from a real translation: in an R script the entity\n```r\n{fx.r_text[:600]}\n```\nscored {fx.score_after} against R "
            f"after the Python was changed to\n```python\n{fx.after[:1500]}\n```\n")
    if fx.before.strip():
        text += f"(it scored {fx.score_before} with\n```python\n{fx.before[:800]}\n```\n)\n"
    return text + ("Use this as evidence of R's behaviour, not as the answer: the function must reproduce R on any input of its "
                   "ordinary kind, not just this call.")

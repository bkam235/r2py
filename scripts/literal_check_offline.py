"""Offline validation of the pasted-R-output check (`r2py/harness/literal_check.py`, 2026-11-11). No model calls.

1. `screen`: the model-screen-stall2 continuations rescored as if the check had gated them: a continuation's final
   is its best accepted step whose program passes the check against the chain's start program (else the start).
   This approximates a gated run (a rejected step would have led elsewhere). Then the gain on the plateau per arm
   against stall2_ps, as in `scripts/model_screen.py`.
2. `flags RUN_DIR...`: every accepted program of other runs checked against its run's frozen start, to read what
   the check flags where pasting was hard (bare probes).

    python scripts/literal_check_offline.py screen
    python scripts/literal_check_offline.py flags work/replay_default_e8 work/ceiling_glm53
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]

import model_screen as ms  # noqa: E402
import replay  # noqa: E402
import stall2_continue as s2  # noqa: E402
from r2py.harness import literal_check as lc  # noqa: E402

_maps: dict = {}


def script_map(script: str):
    if script not in _maps:
        import pickle
        _maps[script] = pickle.load(open(ROOT / "work/reverify/script_maps" / (Path(script).stem + ".pkl"), "rb"))
    return _maps[script]


def screen() -> None:
    ch = s2.chains()
    rows = {**ms._rows(s2.OUT / "results.jsonl"), **ms._rows(ms.OUT / "results.jsonl")}
    gated, flagged = {}, {}
    for k, r in rows.items():
        script, arm, sample = k
        if arm not in ms.ARMS:
            gated[k] = r
            continue
        run_label, b = sample.rsplit(".", 1)
        c = ch[(script, run_label, int(b))]
        f = ms.OUT / "trajectories" / f"{Path(script).stem}.{arm}.{sample}.jsonl"
        recs = [json.loads(l) for l in f.open(encoding="utf-8")] if f.exists() else []
        best, n = float(r["start_score"]), 0
        for a in (x for x in recs if x["kind"] == "accepted" and x.get("source")):
            reason = lc.check(a["source"], c["source"], script_map(script).source, script_map(script))
            if reason:
                n += 1
            else:
                best = max(best, a["aggregate"])
        flagged[arm] = flagged.get(arm, 0) + (n > 0)
        gated[k] = {**r, "final_score": best}
    ref = ms.finals(ch, gated, ms.REF)
    print("chains with a flagged accepted step:", flagged)
    for arm in ms.ARMS[1:]:
        f = ms.finals(ch, gated, arm)
        st_ = sorted(s for s in ref if ref[s] is not None and f.get(s) is not None)
        g = {s: f[s] - ref[s] for s in st_}
        rng = random.Random(0)
        b = sorted(sum(g[rng.choice(st_)] for _ in st_) / 60 for _ in range(10000))
        print(f"  {arm:20s} gated: states {len(st_)}  gain {sum(g.values()) / 60:+.4f} [{b[250]:+.4f}, {b[9749]:+.4f}]  "
              f"P {sum(x > 0 for x in b) / len(b):.2f}")


def flags(run_dirs) -> None:
    states = replay.training_states()
    for d in map(Path, run_dirs):
        n = hit = 0
        for f in sorted((d / "trajectories").glob("*.jsonl")):
            recs = [json.loads(l) for l in f.open(encoding="utf-8")]
            script = recs[0]["script"]
            if script not in states:
                continue
            for a in (x for x in recs if x["kind"] == "accepted" and x.get("source")):
                n += 1
                h = lc.pasted(a["source"], states[script]["source"], script_map(script).source,
                              lc.truth_numbers(script_map(script)))
                if len(h) >= lc.REJECT_AT:
                    hit += 1
                    print(f"  {f.stem[:70]:70s} step {a['step']}: {len(h)} {h[:5]}")
        print(f"{d.name}: {hit} of {n} accepted programs flagged")


if __name__ == "__main__":
    if sys.argv[1] == "screen":
        screen()
    else:
        flags(sys.argv[2:])

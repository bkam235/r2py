"""Patience on crashing programs: continue the chains that stalled while crashing (registered 2026-10-18).

From the width-3 runs of the 3-per-step replay (`work/replay_k3`), every chain that stopped by stalling while its
best program still crashed continues from that program for 2 more steps (policy `continue2`: width 1, fresh
history). Then each width-3 run's final is recomputed with the continued chains substituted.

    python scripts/continue_stalled.py run --workers 8
    python scripts/continue_stalled.py summary
"""
from __future__ import annotations

import argparse
import collections
import json
import multiprocessing
import random
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
SRC = ROOT / "work/replay_k3"
OUT = ROOT / "work/continue_stalled"


def chains() -> dict:
    """(script, sample, branch) -> {start, final (ok, score), source, stalled_crashing} for every width-3 chain."""
    import replay
    from r2py.harness import trajectory
    states = replay.training_states()
    rows = [r for r in map(json.loads, (SRC / "results.jsonl").open(encoding="utf-8")) if r["policy"] == "rewrite_w3"]
    out = {}
    for row in rows:
        recs = [json.loads(l) for l in (SRC / "trajectories" / f"{Path(row['script']).stem}.rewrite_w3.{row['sample']}.jsonl").open(encoding="utf-8")]
        acc = {(r.get("branch"), r["step"]): r for r in recs if r["kind"] == "accepted"}
        ver = {(r.get("branch"), r.get("step")): (r.get("exit_code") == 0, r["aggregate"])
               for r in recs if r["kind"] == "step" and "aggregate" in r}
        steps = collections.defaultdict(set)
        for r in recs:
            if r["kind"] == "step":
                steps[r.get("branch")].add(r["step"])
        for b in (0, 1, 2):
            cur, src = (row["start_exit"] == 0, row["start_score"]), states[row["script"]]["source"]
            for n in sorted(steps[b]):
                if (b, n) in acc and (b, n) in ver:
                    cur, src = ver[(b, n)], acc[(b, n)].get("source") or src
            last = sorted(steps[b])[-3:]
            stalled = len(last) == 3 and not any((b, n) in acc for n in last)
            out[(row["script"], row["sample"], b)] = {"final": cur, "source": src, "start_exit": row["start_exit"],
                                                      "recorded": row["final_score"],
                                                      "stalled_crashing": stalled and not cur[0],
                                                      "hash": trajectory.source_hash(src)}
    return out


def run(workers: int) -> None:
    import replay
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / "results.jsonl"
    done = {(r["script"], r["sample"]) for r in map(json.loads, out.open(encoding="utf-8"))} if out.exists() else set()
    tasks = []
    for (script, sample, b), c in sorted(chains().items()):
        key = f"{sample}.{b}"
        if not c["stalled_crashing"] or (script, key) in done:
            continue
        tasks.append(dict(script=script, policy="continue2", sample=key, source=c["source"], label="continue",
                          start_hash=c["hash"], manifest=str(ROOT / "experiments/dev_run/manifest.json"),
                          library=str(ROOT / "work/dev_run/checkpoints/empty"), runtime_dir=None,
                          cache=str(replay.TRAIN_MAPS), out_dir=str(OUT), budget_s=1200))
    print(f"{len(tasks)} chains to continue, {workers} workers", flush=True)
    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(workers) as pool, out.open("a", encoding="utf-8") as f:
        for i, row in enumerate(pool.imap_unordered(replay.run_one, tasks), 1):
            f.write(json.dumps(row) + "\n")
            f.flush()
            print(f"[{i}/{len(tasks)}] {row['script'][:40]} {row['sample']}: "
                  + (f"{row['start_score']:.2f} -> {row['final_score']:.2f} exit {row['final_exit']}" if "final_score" in row
                     else f"ERROR {row.get('error', '')[:80]}"), flush=True)


def summary() -> None:
    ch = chains()
    cont = {(r["script"], r["sample"]): r for r in map(json.loads, (OUT / "results.jsonl").open(encoding="utf-8"))}
    rows = [r for r in cont.values() if "final_score" in r]
    print(f"{len(rows)} continued chains, errors {len(cont) - len(rows)}")
    print(f"  improved {sum(r['improved'] for r in rows)}/{len(rows)}, now running {sum(r['final_exit'] == 0 for r in rows)}/{len(rows)}, "
          f"mean gain {st.mean(r['final_score'] - r['start_score'] for r in rows):+.3f}")
    runs = collections.defaultdict(dict)
    for (script, sample, b), c in ch.items():
        new = c["final"]
        r = cont.get((script, f"{sample}.{b}"))
        if r and "final_score" in r:
            new = max(new, (r["final_exit"] == 0, r["final_score"]))
        runs[(script, sample)][b] = (c["final"], new, c["start_exit"])
    per_state = collections.defaultdict(list)
    for (script, sample), bs in runs.items():
        old = max(v[0] for v in bs.values())[1]
        new = max(v[1] for v in bs.values())[1]
        per_state[(script, bs[0][2] != 0)].append(new - old)
    rng = random.Random(0)
    for label, crash in (("crashing starts", True), ("running starts", False)):
        d = [st.mean(v) for (s, c), v in per_state.items() if c == crash]
        b = sorted(st.mean(rng.choice(d) for _ in d) for _ in range(5000))
        print(f"  run-level gain, {label} ({len(d)} states): {st.mean(d):+.4f} [{b[125]:+.4f}, {b[4874]:+.4f}]")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "summary"])
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    run(a.workers) if a.cmd == "run" else summary()

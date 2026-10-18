"""Running starts on a plateau: restart with a fresh history, or also accept equal-scoring programs (registered 2026-10-18).

From each width-3 run of the 3-per-step replay (`work/replay_k3`) whose start runs and whose final is below the
threshold, the program the run returned continues for 3 more steps, once per arm, concurrently:
`continue3` (fresh history, strict acceptance) and `continue3_eq` (the same, plus equal-scoring moves).

    python scripts/continue_plateau.py run --workers 8
    python scripts/continue_plateau.py summary
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
OUT = ROOT / "work/continue_plateau"
ARMS = ("continue3", "continue3_eq")
THRESHOLD = 0.9


def plateau_states() -> dict:
    """(script, sample) -> {source, score, hash} of the program each running-start width-3 run returned."""
    from continue_stalled import chains
    runs = collections.defaultdict(list)
    for (script, sample, b), c in chains().items():
        runs[(script, sample)].append(c)
    out = {}
    for key, cs in runs.items():
        if cs[0]["start_exit"] != 0:
            continue
        best = max(cs, key=lambda c: c["final"])
        if best["final"][0] and best["final"][1] < THRESHOLD:
            out[key] = {"source": best["source"], "score": best["final"][1], "hash": best["hash"]}
    return out


def run(workers: int) -> None:
    import replay
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / "results.jsonl"
    done = {(r["script"], r["policy"], r["sample"]) for r in map(json.loads, out.open(encoding="utf-8"))} if out.exists() else set()
    tasks = []
    for (script, sample), s in sorted(plateau_states().items()):
        for arm in ARMS:
            if (script, arm, sample) in done:
                continue
            tasks.append(dict(script=script, policy=arm, sample=sample, source=s["source"], label="plateau",
                              start_hash=s["hash"], manifest=str(ROOT / "experiments/dev_run/manifest.json"),
                              library=str(ROOT / "work/dev_run/checkpoints/empty"), runtime_dir=None,
                              cache=str(replay.TRAIN_MAPS), out_dir=str(OUT), budget_s=1200))
    print(f"{len(tasks)} continuations, {workers} workers", flush=True)
    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(workers) as pool, out.open("a", encoding="utf-8") as f:
        for i, row in enumerate(pool.imap_unordered(replay.run_one, tasks), 1):
            f.write(json.dumps(row) + "\n")
            f.flush()
            print(f"[{i}/{len(tasks)}] {row['script'][:40]} {row['policy']} s{row['sample']}: "
                  + (f"{row['start_score']:.3f} -> {row['final_score']:.3f}" if "final_score" in row
                     else f"ERROR {row.get('error', '')[:80]}"), flush=True)


def summary() -> None:
    rows = [r for r in map(json.loads, (OUT / "results.jsonl").open(encoding="utf-8"))]
    ok = [r for r in rows if "final_score" in r]
    print(f"{len(ok)} continuations, errors {len(rows) - len(ok)}")
    rng = random.Random(0)
    per = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in ok:
        per[r["policy"]][r["script"]].append(r["final_score"] - r["start_score"])
    for arm in ARMS:
        rs = [r for r in ok if r["policy"] == arm]
        moves = sum(r["agent"].get("outcome", {}).get("rewrite:equal_move", 0) for r in rs)
        d = [st.mean(v) for v in per[arm].values()]
        b = sorted(st.mean(rng.choice(d) for _ in d) for _ in range(5000))
        print(f"{arm:<13} runs {len(rs)}  improved {sum(r['improved'] for r in rs)}  equal moves {moves}  "
              f"gain over the plateau (per state, {len(d)}): {st.mean(d):+.4f} [{b[125]:+.4f}, {b[4874]:+.4f}]")
    ks = sorted(set(per[ARMS[0]]) & set(per[ARMS[1]]))
    d = [st.mean(per[ARMS[1]][k]) - st.mean(per[ARMS[0]][k]) for k in ks]
    b = sorted(st.mean(rng.choice(d) for _ in d) for _ in range(5000))
    print(f"equal moves - restart, paired ({len(ks)} states): {st.mean(d):+.4f} [{b[125]:+.4f}, {b[4874]:+.4f}]")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "summary"])
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    run(a.workers) if a.cmd == "run" else summary()

"""Stop threshold 0.95 under the DeepSeek default (test `threshold-095`, registered 2026-11-15).

Source: the replay of `default_2026_11_12` on the 60 training starts (`work/dsflash_default`, run as policy
`default_2026_11_01_dsflash`). On this pool a threshold of 0.95 can change only the states whose final is in
[0.9, 0.95) (finals re-verified under epoch 11, `finals_epoch11.jsonl`): a state below 0.9 has no chain that reached
0.9, a state >= 0.95 is there already. Two arms, both one chain of the default loop (width 1, conversation, entity
feedback, DeepSeek agent, in-state free probes, review + literal_check):
- `t95_cont` (threshold 0.95): every chain of those states whose best (as logged) is in [0.9, 0.95), i.e. that
  stopped at the 0.9 threshold, continues from its best program with a fresh conversation and stall budget;
- `t90_chain` (sampling, the comparator): 3 more independent chains per state from the frozen start at 0.9.

Analysis: per state, final(arm) = max(recorded final, the arm's chain finals); flipped = final(arm) >= 0.95 and the
recorded final < 0.95 (all of these states). Primary: share gain of each arm (flipped / 60) and states flipped per
call, t95 minus t90, bootstrap over states, P(> 0). Secondary: gain on the plateau (sum / 60), calls, cost, "done"s.

    python scripts/threshold95_continue.py chains
    python scripts/threshold95_continue.py run --workers 6 --budget 1 [--limit 1 --out work/x]
    python scripts/threshold95_continue.py analyze
"""
from __future__ import annotations

import argparse
import collections
import json
import multiprocessing
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
SRC = ROOT / "work/dsflash_default"
POLICY = "default_2026_11_01_dsflash"
OUT = ROOT / "work/threshold95"
LOW, HIGH = 0.9, 0.95
EXTRA_CHAINS = 3
ARMS = ("t95_cont", "t90_chain")


def finals() -> dict:
    """script -> the default's final re-verified under epoch 11."""
    return {f"{r['stem']}.R": r["aggregate"]
            for r in map(json.loads, (SRC / "finals_epoch11.jsonl").open(encoding="utf-8"))}


def recorded() -> dict:
    return {r["script"]: r for r in map(json.loads, (SRC / "results.jsonl").open(encoding="utf-8"))}


def chains() -> dict:
    """(script, branch) -> {best, source, hash} of every chain of the states whose final is in [LOW, HIGH)."""
    import replay
    from r2py.harness import trajectory
    states = replay.training_states()
    fin, rec = finals(), recorded()
    out = {}
    for script, row in rec.items():
        if not LOW <= fin[script] < HIGH:
            continue
        recs = [json.loads(l) for l in (SRC / "trajectories" / f"{Path(script).stem}.{POLICY}.{row['sample']}.jsonl")
                .open(encoding="utf-8")]
        branches = {r["branch"] for r in recs if r["kind"] == "step" and r.get("branch") is not None}
        for b in sorted(branches):
            src, best = states[script]["source"], row["start_score"]
            for r in recs:   # in the order written: the last accepted program is the chain's best
                if r["kind"] == "accepted" and r.get("branch") == b:
                    src, best = trajectory.program(r) or src, r["aggregate"]
            out[(script, b)] = dict(best=best, source=src, hash=trajectory.source_hash(src))
    return out


def tasks(limit=None) -> list:
    import replay
    states = replay.training_states()
    common = dict(manifest=str(ROOT / "experiments/dev_run/manifest.json"), label="threshold95",
                  library=str(ROOT / "work/dev_run/checkpoints/empty"), runtime_dir=None,
                  cache=str(replay.TRAIN_MAPS), budget_s=1200)
    ch = chains()
    out = []
    for script in sorted({s for s, _ in ch})[:limit]:
        for (s, b), c in sorted(ch.items()):
            if s == script and LOW <= c["best"] < HIGH:
                out.append(dict(script=script, policy="t95_cont", sample=f"b{b}", source=c["source"],
                                start_hash=c["hash"], **common))
        for k in range(EXTRA_CHAINS):
            out.append(dict(script=script, policy="t90_chain", sample=f"c{k}", source=states[script]["source"],
                            start_hash=states[script]["hash"], **common))
    return out


def run(workers: int, budget: float, reserve: float, out_dir=OUT, limit=None) -> None:
    import replay
    from expkit import RunGuard
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "results.jsonl"
    done = {(r["script"], r["policy"], r["sample"]) for r in map(json.loads, out.open(encoding="utf-8"))
            if "final_score" in r and not r.get("invalid")} if out.exists() else set()
    todo = [{**t, "out_dir": str(out_dir)} for t in tasks(limit) if (t["script"], t["policy"], t["sample"]) not in done]
    print(f"{len(todo)} chains to run, {workers} workers", flush=True)
    ctx = multiprocessing.get_context("spawn")
    with RunGuard(out_dir, budget=budget, reserve=reserve) as guard, ctx.Pool(workers) as pool, \
            out.open("a", encoding="utf-8") as f:
        for i, row in enumerate(pool.imap_unordered(replay.run_one, todo), 1):
            row = guard.annotate(row)
            f.write(json.dumps(row) + "\n")
            f.flush()
            print(f"[{i}/{len(todo)}] {row['script'][:36]:36s} {row['policy']:9s} {row['sample']}: "
                  + (f"{row['start_score']:.3f} -> {row['final_score']:.3f}, {row['llm_steps']} calls"
                     if "final_score" in row else f"ERROR {row.get('error', '')[:80]}"), flush=True)
            if guard.should_stop():
                print(f"[guard] stopping: {guard.stop_reason}", flush=True)
                pool.terminate()
                break


def _valid(r: dict) -> bool:
    if "final_score" not in r or r.get("invalid"):
        return False
    # an agent model that was never called (blocked, failing) leaves an ordinary-looking row: not valid
    return r["agent_model"].removeprefix("openrouter:") in (r.get("usage") or {})


def analyze(out_dir=OUT) -> None:
    fin = finals()
    want = collections.Counter((t["script"], t["policy"]) for t in tasks())
    rows = collections.defaultdict(list)
    for r in map(json.loads, (out_dir / "results.jsonl").open(encoding="utf-8")):
        if _valid(r):
            rows[(r["script"], r["policy"])].append(r)
    states = sorted({s for s, _ in want if all(len(rows[(s, a)]) == want[(s, a)] for a in ARMS)})
    print(f"states {len(states)} of {len({s for s, _ in want})} complete")
    flip, gain, calls = ({a: {} for a in ARMS} for _ in range(3))
    for a in ARMS:
        rs = [r for s in states for r in rows[(s, a)]]
        acts, cost = collections.Counter(), 0.0
        for r in rs:
            acts.update(r["agent"]["action"])
            cost += sum(u["cost"] for u in (r.get("usage") or {}).values())
        print(f"  {a:9s} chains {len(rs):3d}  improved {sum(r['final_score'] > r['start_score'] for r in rs):3d}  "
              f"reach >= {HIGH} {sum(r['final_score'] >= HIGH for r in rs):3d}  calls {sum(r['llm_steps'] for r in rs):4d}  "
              f"done {acts.get('done', 0):3d}  probes {acts.get('probe_r', 0):3d}  cost ${cost:.2f}")
        for s in states:
            new = max([fin[s]] + [r["final_score"] for r in rows[(s, a)]])
            flip[a][s] = float(new >= HIGH)
            gain[a][s] = new - fin[s]
            calls[a][s] = sum(r["llm_steps"] for r in rows[(s, a)])

    def stats(smp):
        f = {a: sum(flip[a][s] for s in smp) for a in ARMS}
        n = {a: sum(calls[a][s] for s in smp) for a in ARMS}
        pc = {a: f[a] / n[a] if n[a] else 0.0 for a in ARMS}
        return (f["t95_cont"] / 60, f["t90_chain"] / 60, pc["t95_cont"] - pc["t90_chain"],
                sum(gain["t95_cont"][s] for s in smp) / 60, sum(gain["t90_chain"][s] for s in smp) / 60)

    point = stats(states)
    rng = random.Random(0)
    boots = [stats([rng.choice(states) for _ in states]) for _ in range(10000)]
    for i, name in enumerate(("t95: share gain", "t90: share gain", "flipped per call, t95 - t90",
                              "t95: gain on the plateau", "t90: gain on the plateau")):
        c = sorted(b[i] for b in boots)
        print(f"{name:30s} {point[i]:+.5f} [{c[250]:+.5f}, {c[9749]:+.5f}]  P(> 0) {sum(x > 0 for x in c) / len(c):.3f}")
    for s in states:
        print(f"  {s[:46]:46s} {fin[s]:.3f}  t95 {gain['t95_cont'][s]:+.3f} ({calls['t95_cont'][s]} calls)"
              f"  t90 {gain['t90_chain'][s]:+.3f} ({calls['t90_chain'][s]} calls)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["chains", "run", "analyze"])
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--budget", type=float, default=1.0)
    ap.add_argument("--reserve", type=float, default=0.5)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    if a.cmd == "chains":
        t = tasks()
        for x in t:
            print(f"  {x['policy']:9s} {x['sample']:3s} {x['script']}")
        print(f"{len({x['script'] for x in t})} states; " + ", ".join(
            f"{p} {sum(x['policy'] == p for x in t)} chains" for p in ARMS))
    elif a.cmd == "run":
        run(a.workers, a.budget, a.reserve, out_dir=Path(a.out), limit=a.limit)
    else:
        analyze(Path(a.out))

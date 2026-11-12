"""Patience under the DeepSeek default (test `patience-dsflash`, registered 2026-11-12).

Source: the replay of `default_2026_11_12` on the 60 training starts (`work/dsflash_default`, run as policy
`default_2026_11_01_dsflash`). States: the 19 whose final is below 0.9. Two arms, both one chain of the default
loop (width 1, conversation, entity feedback, DeepSeek agent, in-state free probes, review + literal_check):
- `dsf_cont` (patience): every chain of those states whose best is below 0.9 continues from its best program, with a
  fresh conversation and a fresh stall budget (3 failed rewrites while running, 5 while crashing);
- `dsf_chain` (width, the comparator): 3 more independent chains per state from the frozen start.

Analysis: per state, final(arm) = max(recorded final, the arm's chain finals); gain = final(arm) - recorded final;
calls = the arm's agent calls. Primary: gain per call of patience minus gain per call of width (sums over states),
bootstrap over states, P(> 0). Secondary: gain on the plateau of each arm (sum / 60) with 95% intervals, chains
improved, "done"s, probes, cost.

    python scripts/patience_continue.py chains
    python scripts/patience_continue.py run --workers 6 --budget 4 [--limit 1 --out work/x]
    python scripts/patience_continue.py analyze
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
SRC = ROOT / "work/dsflash_default"
POLICY = "default_2026_11_01_dsflash"
OUT = ROOT / "work/patience_dsflash"
THRESHOLD = 0.9
EXTRA_CHAINS = 3


def recorded() -> dict:
    """script -> results row of the source run."""
    return {r["script"]: r for r in map(json.loads, (SRC / "results.jsonl").open(encoding="utf-8"))}


def chains() -> dict:
    """(script, branch) -> {best, source, hash} of every chain, in the states whose final is below the threshold."""
    import replay
    from r2py.harness import trajectory
    states = replay.training_states()
    out = {}
    for script, row in recorded().items():
        if row["final_score"] >= THRESHOLD:
            continue
        recs = [json.loads(l) for l in (SRC / "trajectories" / f"{Path(script).stem}.{POLICY}.{row['sample']}.jsonl")
                .open(encoding="utf-8")]
        branches = {r["branch"] for r in recs if r["kind"] == "step" and r.get("branch") is not None}
        for b in sorted(branches):
            src, best = states[script]["source"], row["start_score"]
            for r in recs:   # in the order written: the last accepted program is the chain's best
                if r["kind"] == "accepted" and r.get("branch") == b:
                    src, best = r.get("source") or src, r["aggregate"]
            out[(script, b)] = dict(best=best, source=src, hash=trajectory.source_hash(src))
    return out


def tasks(limit=None) -> list:
    import replay
    states = replay.training_states()
    common = dict(manifest=str(ROOT / "experiments/dev_run/manifest.json"), label="patience",
                  library=str(ROOT / "work/dev_run/checkpoints/empty"), runtime_dir=None,
                  cache=str(replay.TRAIN_MAPS), budget_s=1200)
    ch = chains()
    scripts = sorted({s for s, _ in ch})[:limit]
    out = []
    for script in scripts:
        for (s, b), c in sorted(ch.items()):
            if s == script and c["best"] < THRESHOLD:
                out.append(dict(script=script, policy="dsf_cont", sample=f"b{b}", source=c["source"],
                                start_hash=c["hash"], **common))
        for k in range(EXTRA_CHAINS):
            out.append(dict(script=script, policy="dsf_chain", sample=f"c{k}", source=states[script]["source"],
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
    return float(r["start_score"]) >= THRESHOLD or r["agent_model"].removeprefix("openrouter:") in (r.get("usage") or {})


def analyze(out_dir=OUT) -> None:
    rec = recorded()
    want = collections.Counter((t["script"], t["policy"]) for t in tasks())
    rows = collections.defaultdict(list)
    for r in map(json.loads, (out_dir / "results.jsonl").open(encoding="utf-8")):
        if _valid(r):
            rows[(r["script"], r["policy"])].append(r)
    states = sorted({s for s, _ in want if all(len(rows[(s, a)]) == want[(s, a)] for a in ("dsf_cont", "dsf_chain"))})
    print(f"states {len(states)} of {len({s for s, _ in want})} complete")
    gain, calls = {a: {} for a in ("dsf_cont", "dsf_chain")}, {a: {} for a in ("dsf_cont", "dsf_chain")}
    for a in gain:
        rs = [r for s in states for r in rows[(s, a)]]
        acts, cost = collections.Counter(), 0.0
        for r in rs:
            acts.update(r["agent"]["action"])
            cost += sum(u["cost"] for u in (r.get("usage") or {}).values())
        print(f"  {a:9s} chains {len(rs):3d}  improved {sum(r['final_score'] > r['start_score'] for r in rs):3d}  "
              f"reach >= 0.9 {sum(r['final_score'] >= THRESHOLD for r in rs):3d}  calls {sum(r['llm_steps'] for r in rs):4d}  "
              f"done {acts.get('done', 0):3d}  probes {acts.get('probe_r', 0):3d}  cost ${cost:.2f}")
        for s in states:
            base = rec[s]["final_score"]
            gain[a][s] = max([base] + [r["final_score"] for r in rows[(s, a)]]) - base
            calls[a][s] = sum(r["llm_steps"] for r in rows[(s, a)])

    def stats(smp):
        g = {a: sum(gain[a][s] for s in smp) for a in gain}
        n = {a: sum(calls[a][s] for s in smp) for a in gain}
        pc = {a: g[a] / n[a] if n[a] else 0.0 for a in gain}
        return g["dsf_cont"] / 60, g["dsf_chain"] / 60, pc["dsf_cont"], pc["dsf_chain"], pc["dsf_cont"] - pc["dsf_chain"]

    point = stats(states)
    rng = random.Random(0)
    boots = [stats([rng.choice(states) for _ in states]) for _ in range(10000)]
    ci = lambda i: sorted(b[i] for b in boots)
    for i, name in enumerate(("patience: gain on the plateau", "width: gain on the plateau",
                              "patience: gain per call", "width: gain per call", "per call, patience - width")):
        c = ci(i)
        print(f"{name:32s} {point[i]:+.5f} [{c[250]:+.5f}, {c[9749]:+.5f}]  P(> 0) {sum(x > 0 for x in c) / len(c):.3f}")
    for s in sorted(states, key=lambda s: -max(gain["dsf_cont"][s], gain["dsf_chain"][s]))[:12]:
        print(f"  {s[:46]:46s} {rec[s]['final_score']:.3f}  patience {gain['dsf_cont'][s]:+.3f} ({calls['dsf_cont'][s]} calls)"
              f"  width {gain['dsf_chain'][s]:+.3f} ({calls['dsf_chain'][s]} calls)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["chains", "run", "analyze"])
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--budget", type=float, default=4.0)
    ap.add_argument("--reserve", type=float, default=0.5)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    if a.cmd == "chains":
        t = tasks()
        print(f"{len({x['script'] for x in t})} states; " + ", ".join(
            f"{p} {sum(x['policy'] == p for x in t)} chains" for p in ("dsf_cont", "dsf_chain")))
    elif a.cmd == "run":
        run(a.workers, a.budget, a.reserve, out_dir=Path(a.out), limit=a.limit)
    else:
        analyze(Path(a.out))

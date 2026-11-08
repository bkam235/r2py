"""The stall-2 step (test `free-probe-stall2`, registered 2026-11-08): continue saved chains at the point where two
rewrites in a row have failed, once with the default stall hint ("Try probe_r ... or action:done") and once with
free probes (a probe costs no stall and shows its result; the hint points at the probe and offers no "done").

Chains: every chain of the default's two e8 replays (`work/replay_default_e8`, `work/replay_default_e8_s1`) that
reaches two non-improving steps in a row while its best program runs; the first such point per chain. Each is
continued from its best program at that point (width 1, conversation and entity feedback as in the default, the
stall count starting at 2, so the hint comes before the first call; at most 8 steps). Both arms start from the same
program and the same turn, so each chain is its own pair.

Analysis: each run's final is recomputed with every continued chain's result in place of what the chain did after
its stall-2 point (chains that never reached it keep their recorded best), once per arm. Per state (mean over its
runs): gain = final(free probe) - final(default hint), extra calls = calls(free probe) - calls(default hint).
Primary: gain per extra call against one more chain (0.00148 per call, `width6-running-pool`), bootstrap over
states, P(better). Secondary: chain-level improvement rates, probes and "done"s per arm, gain on the plateau.

    python scripts/stall2_continue.py chains
    python scripts/stall2_continue.py run --workers 6 --budget 4.00
    python scripts/stall2_continue.py analyze
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
SRC = (ROOT / "work/replay_default_e8", ROOT / "work/replay_default_e8_s1")
POLICY = "default_2026_11_01"
OUT = ROOT / "work/stall2_continue"
ARMS = ("stall2_default", "stall2_fp")
WIDTH_PER_CALL = 0.00148


def chains() -> dict:
    """(script, run label, branch) -> {source, score, recorded best of the chain, reached} for every chain."""
    import replay
    from r2py.harness import trajectory
    states = replay.training_states()
    out = {}
    for d in SRC:
        for row in map(json.loads, (d / "results.jsonl").open(encoding="utf-8")):
            stem = Path(row["script"]).stem
            recs = [json.loads(l) for l in (d / "trajectories" / f"{stem}.{POLICY}.{row['sample']}.jsonl").open(encoding="utf-8")]
            acc = {(r.get("branch"), r["step"]): r for r in recs if r["kind"] == "accepted"}
            verified = {(r.get("branch"), r["step"]): r for r in recs
                        if r["kind"] == "step" and "aggregate" in r and (r.get("branch"), r["step"]) in acc}
            steps = collections.defaultdict(set)
            for r in recs:
                if r["kind"] in ("step", "done") and r.get("branch") is not None:
                    steps[r["branch"]].add(r["step"])
            for b, ss in steps.items():
                src, score, ok = states[row["script"]]["source"], row["start_score"], row["start_exit"] == 0
                stall, point = 0, None
                best = score
                for s in sorted(ss):
                    if (b, s) in acc:
                        stall = 0
                        src = acc[(b, s)].get("source") or src
                        score = acc[(b, s)]["aggregate"]
                        ok = verified[(b, s)]["exit_code"] == 0 if (b, s) in verified else ok
                        best = max(best, score)
                    else:
                        stall += 1
                    if stall == 2 and ok and point is None:
                        point = dict(source=src, score=score)
                run = f"{d.name}.{row['sample']}"
                out[(row["script"], run, b)] = dict(best=best, reached=point is not None, start=row["start_score"],
                                                    start_exit=row["start_exit"],
                                                    **({"source": point["source"], "score": point["score"],
                                                        "hash": trajectory.source_hash(point["source"])} if point else {}))
    return out


def run(workers: int, budget: float, reserve: float, arms=ARMS, out_dir=OUT, limit=None) -> None:
    import replay
    from expkit import RunGuard
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "results.jsonl"
    done = {(r["script"], r["policy"], r["sample"]) for r in map(json.loads, out.open(encoding="utf-8"))
            if "final_score" in r and not r.get("invalid")} if out.exists() else set()
    tasks = []
    reached = [(k, c) for k, c in sorted(chains().items()) if c["reached"]]
    for (script, run_label, b), c in reached[:limit]:
        for arm in arms:
            key = f"{run_label}.{b}"
            if (script, arm, key) in done:
                continue
            tasks.append(dict(script=script, policy=arm, sample=key, source=c["source"], label="stall2",
                              start_hash=c["hash"], manifest=str(ROOT / "experiments/dev_run/manifest.json"),
                              library=str(ROOT / "work/dev_run/checkpoints/empty"), runtime_dir=None,
                              cache=str(replay.TRAIN_MAPS), out_dir=str(out_dir), budget_s=1200))
    print(f"{len(tasks)} continuations to run, {workers} workers", flush=True)
    ctx = multiprocessing.get_context("spawn")
    with RunGuard(out_dir, budget=budget, reserve=reserve) as guard, ctx.Pool(workers) as pool, \
            out.open("a", encoding="utf-8") as f:
        for i, row in enumerate(pool.imap_unordered(replay.run_one, tasks), 1):
            row = guard.annotate(row)
            f.write(json.dumps(row) + "\n")
            f.flush()
            print(f"[{i}/{len(tasks)}] {row['script'][:36]:36s} {row['policy']:14s} {row['sample']}: "
                  + (f"{row['start_score']:.3f} -> {row['final_score']:.3f}, {row['llm_steps']} calls"
                     if "final_score" in row else f"ERROR {row.get('error', '')[:80]}"), flush=True)
            if guard.should_stop():
                print(f"[guard] stopping: {guard.stop_reason}", flush=True)
                pool.terminate()
                break


def analyze() -> None:
    ch = chains()
    rows = {(r["script"], r["policy"], r["sample"]): r for r in map(json.loads, (OUT / "results.jsonl").open(encoding="utf-8"))
            if "final_score" in r and not r.get("invalid")}
    pairs = [(k, rows.get((k[0], ARMS[0], f"{k[1]}.{k[2]}")), rows.get((k[0], ARMS[1], f"{k[1]}.{k[2]}")))
             for k, c in ch.items() if c["reached"]]
    complete = [(k, a, b) for k, a, b in pairs if a and b]
    print(f"chains at stall 2: {len(pairs)}, both arms finished: {len(complete)}")
    for i, arm in enumerate(ARMS):
        rs = [p[1 + i] for p in complete]
        acts = collections.Counter()
        for r in rs:
            acts.update(r["agent"]["action"])
        print(f"  {arm:14s} improved {sum(r['improved'] for r in rs)}/{len(rs)}  mean gain "
              f"{st.mean(r['final_score'] - r['start_score'] for r in rs):+.4f}  calls {sum(r['llm_steps'] for r in rs)}  "
              f"actions {dict(acts)}")
    cont = {k: (a, b) for k, a, b in complete}
    runs = collections.defaultdict(dict)
    for (script, run_label, b), c in ch.items():
        runs[(script, run_label)][b] = c
    per_state = collections.defaultdict(lambda: {"gain": [], "extra": []})
    for (script, run_label), bs in runs.items():
        finals, calls = [], []
        for i in (0, 1):
            best, n = max(c["start"] for c in bs.values()), 0
            for b, c in bs.items():
                if c["reached"] and (script, run_label, b) in cont:
                    r = cont[(script, run_label, b)][i]
                    best = max(best, r["final_score"], c["score"])
                    n += r["llm_steps"]
                else:
                    best = max(best, c["best"])
            finals.append(best)
            calls.append(n)
        per_state[script]["gain"].append(finals[1] - finals[0])
        per_state[script]["extra"].append(calls[1] - calls[0])
    states = sorted(per_state)
    g = {s: st.mean(per_state[s]["gain"]) for s in states}
    e = {s: st.mean(per_state[s]["extra"]) for s in states}
    total_gain, total_extra = sum(g.values()), sum(e.values())
    rng = random.Random(0)
    boots, per_call = [], []
    for _ in range(10000):
        smp = [rng.choice(states) for _ in states]
        tg, te = sum(g[s] for s in smp), sum(e[s] for s in smp)
        boots.append(tg / 60)
        per_call.append(tg / te if te > 0 else float("inf") if tg > 0 else 0.0)
    boots.sort(); per_call.sort()
    p_better = sum(x > WIDTH_PER_CALL for x in per_call) / len(per_call)
    print(f"states {len(states)}; gain on the plateau (sum over states / 60) {total_gain / 60:+.4f} "
          f"[{boots[250]:+.4f}, {boots[9749]:+.4f}]; extra calls {total_extra:+.1f}")
    print(f"gain per extra call {total_gain / total_extra if total_extra else float('nan'):.5f} "
          f"[{per_call[250]:.5f}, {per_call[9749]:.5f}] against one more chain {WIDTH_PER_CALL}: P(better) {p_better:.2f}")
    for s in sorted(states, key=lambda s: -abs(g[s]))[:10]:
        print(f"  {s[:50]:50s} gain {g[s]:+.3f}  extra calls {e[s]:+.1f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["chains", "run", "analyze"])
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--budget", type=float, default=4.0)
    ap.add_argument("--reserve", type=float, default=0.5)
    a = ap.parse_args()
    if a.cmd == "chains":
        c = chains()
        r = [v for v in c.values() if v["reached"]]
        print(f"{len(c)} chains, {len(r)} reach stall 2 with a running best, in {len({k[0] for k, v in c.items() if v['reached']})} states")
    elif a.cmd == "run":
        run(a.workers, a.budget, a.reserve)
    else:
        analyze()

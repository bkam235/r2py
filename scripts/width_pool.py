"""Best of k chains from pooled replays of one policy (registered 2026-11-06, test `width6-running-pool`).

Two replays of the same policy from the same frozen starts give independent chains per state. Each chain's best is
the highest accepted aggregate on its branch (the start if it accepted none); a run's final is the best of its chains.
For k = 1..K (K = all chains of a state), the mean over all k-subsets of a state's chains of their best; then the
difference best-of-K minus best-of-3 paired by state, with bootstrap intervals over states. best-of-3 is averaged over
all 3-subsets, so it uses both replays alike. Also the replay-to-replay difference of the two finals (noise of one
sample of the same policy).

    python scripts/width_pool.py work/replay_default_e8 work/replay_default_e8_s1 --stratum running
"""
from __future__ import annotations

import argparse
import collections
import itertools
import json
import random
import statistics as st
from pathlib import Path


def chains(run_dir: Path, policy: str) -> dict:
    """script stem -> {"start", "final", "start_exit", "calls", "chains": [best per branch]}."""
    out = {}
    for row in map(json.loads, (run_dir / "results.jsonl").open(encoding="utf-8")):
        if row["policy"] != policy or row.get("invalid") or "final_score" not in row:
            continue
        stem = Path(row["script"]).stem
        best = {}
        traj = run_dir / "trajectories" / f"{stem}.{policy}.{row['sample']}.jsonl"
        for r in map(json.loads, traj.open(encoding="utf-8")):
            if r.get("branch") is None:
                continue
            b = best.setdefault(r["branch"], row["start_score"])
            if r["kind"] == "accepted":
                best[r["branch"]] = max(b, r["aggregate"])
        out[stem] = dict(start=row["start_score"], final=row["final_score"], start_exit=row["start_exit"],
                         calls=row["llm_steps"], chains=list(best.values()))
    return out


def best_of(chs: list[float], start: float, k: int) -> float:
    if not chs:
        return start
    k = min(k, len(chs))
    return st.mean(max(c) for c in itertools.combinations(chs, k))


def boot(d, n=10000, seed=0):
    rng = random.Random(seed)
    m = sorted(st.mean(rng.choices(d, k=len(d))) for _ in range(n))
    return m


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs=2)
    ap.add_argument("--policy", default="default_2026_11_01")
    ap.add_argument("--stratum", choices=["running", "crashing", "all"], default="running")
    ap.add_argument("--small", type=float, default=0.01, help="|difference| below this counts as tied")
    a = ap.parse_args()
    A, B = (chains(Path(d), a.policy) for d in a.dirs)
    states = sorted(s for s in A.keys() & B.keys()
                    if a.stratum == "all" or (A[s]["start_exit"] == 0) == (a.stratum == "running"))
    print(f"{len(states)} states in both replays ({a.stratum} starts)")
    K = max(len(A[s]["chains"]) + len(B[s]["chains"]) for s in states)
    curve = collections.defaultdict(list)
    for s in states:
        chs = A[s]["chains"] + B[s]["chains"]
        for k in range(1, K + 1):
            curve[k].append(best_of(chs, A[s]["start"], k))
    print("best of k chains (mean over states of the mean over k-subsets):")
    for k in range(1, K + 1):
        print(f"  k={k}: {st.mean(curve[k]):.4f}" + (f"  (+{st.mean(curve[k]) - st.mean(curve[k - 1]):.4f})" if k > 1 else ""))
    calls = [A[s]["calls"] + B[s]["calls"] for s in states]
    nch = sum(len(A[s]["chains"]) + len(B[s]["chains"]) for s in states)
    print(f"calls: {sum(calls)} for {nch} chains, {sum(calls) / max(nch, 1):.2f} per chain")

    def paired(name, d):
        m = boot(d)
        lo, hi = m[int(0.025 * len(m))], m[int(0.975 * len(m)) - 1]
        lo9, hi9 = m[int(0.05 * len(m))], m[int(0.95 * len(m)) - 1]
        p = sum(x > 0 for x in m) / len(m)
        better = sum(x > a.small for x in d); worse = sum(x < -a.small for x in d)
        print(f"{name}: {st.mean(d):+.4f} [{lo:+.4f}, {hi:+.4f}] (90% [{lo9:+.4f}, {hi9:+.4f}]), P(>0) {p:.2f}, "
              f"{better} better / {worse} worse / {len(d) - better - worse} tied")

    paired(f"best of {K} - best of 3, paired by state", [x - y for x, y in zip(curve[K], curve[3])])
    paired("replay 2 final - replay 1 final (same policy), paired by state", [B[s]["final"] - A[s]["final"] for s in states])
    print(f"finals: replay 1 {st.mean(A[s]['final'] for s in states):.4f}, replay 2 {st.mean(B[s]['final'] for s in states):.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Test refuse-done (registered 2026-11-06): what refusing "done" below the threshold gained, inside each run.

Chains of a run are independent, and a chain is the same as the default's up to its first refused "done". So each
run of the policy with `refuse_done` also holds its counterfactual under the default: every chain cut at its first
refused "done" (its best = the start or the best program it accepted before that step). Per state (mean over
samples): gain = final - counterfactual final; extra calls = steps a chain ran after its first refused "done".
Primary: gain per extra call against the marginal gain per call of one more chain (width 5 -> 6 on running starts,
test `width6-running-pool`: +0.0055 per state at 3.72 calls per chain), bootstrap over states. Also every logged
"done" with the model's words, for reading.

    python scripts/refuse_done_analysis.py work/refuse_done --width-per-call 0.00148
    python scripts/refuse_done_analysis.py work/refuse_done --reasons > work/refuse_done/done_reasons.md
"""
from __future__ import annotations

import argparse
import collections
import json
import random
import statistics as st
from pathlib import Path


def runs(run_dir: Path, policy: str):
    for row in map(json.loads, (run_dir / "results.jsonl").open(encoding="utf-8")):
        if row["policy"] != policy or row.get("invalid") or "final_score" not in row:
            continue
        stem = Path(row["script"]).stem
        recs = [json.loads(l) for l in (run_dir / "trajectories" / f"{stem}.{policy}.{row['sample']}.jsonl")
                .open(encoding="utf-8")]
        yield stem, row, recs


def counterfactual(row: dict, recs: list) -> dict:
    cut = {}                                    # branch -> step of its first refused "done"
    for r in recs:
        if r["kind"] == "done" and r.get("refused") and r.get("branch") not in cut:
            cut[r.get("branch")] = r["step"]
    best, best_cf = row["start_score"], row["start_score"]
    steps_after = collections.defaultdict(set)
    for r in recs:
        b = r.get("branch")
        if r["kind"] == "accepted":
            best = max(best, r["aggregate"])
            if b not in cut or r["step"] < cut[b]:
                best_cf = max(best_cf, r["aggregate"])
        if r["kind"] == "step" and b in cut and r["step"] > cut[b]:
            steps_after[b].add(r["step"])
    return dict(final=row["final_score"], best=best, final_cf=best_cf, refused=len(cut),
                extra_calls=sum(len(v) for v in steps_after.values()),
                improved_after=sum(1 for r in recs if r["kind"] == "accepted" and r.get("branch") in cut
                                   and r["step"] > cut[r.get("branch")]))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--policy", default="default_2026_11_01_rd")
    ap.add_argument("--width-per-call", type=float, default=0.00148)
    ap.add_argument("--n-states", type=int, default=60, help="states of the pool, for the effect on the plateau")
    ap.add_argument("--reasons", action="store_true", help="print every logged done with the model's words")
    a = ap.parse_args()
    if a.reasons:
        for stem, row, recs in runs(Path(a.run_dir), a.policy):
            for r in recs:
                if r["kind"] == "done":
                    print(f"## {stem} s{row['sample']} branch {r.get('branch')} step {r['step']}: best "
                          f"{r.get('best_score')}, stalls before {r.get('stall_count')}, "
                          f"{'refused' if r.get('refused') else 'accepted'}\n\n```\n{r['raw'].strip()[-1500:]}\n```\n")
        return 0
    by = collections.defaultdict(list)
    for stem, row, recs in runs(Path(a.run_dir), a.policy):
        by[stem].append(counterfactual(row, recs))
    states = sorted(by)
    gain = [st.mean(c["final"] - c["final_cf"] for c in by[s]) for s in states]
    calls = [st.mean(c["extra_calls"] for c in by[s]) for s in states]
    tot = lambda key: sum(c[key] for s in states for c in by[s])
    print(f"{len(states)} states, {sum(len(v) for v in by.values())} runs; refused dones (chains) {tot('refused')}, "
          f"steps after them {tot('extra_calls')}, improvements accepted after them {tot('improved_after')}")
    print(f"mean final {st.mean(st.mean(c['final'] for c in by[s]) for s in states):.4f}, "
          f"counterfactual (default) {st.mean(st.mean(c['final_cf'] for c in by[s]) for s in states):.4f}")
    rng = random.Random(0)
    boots_g, boots_r = [], []
    for _ in range(10000):
        idx = rng.choices(range(len(states)), k=len(states))
        g, c = sum(gain[i] for i in idx), sum(calls[i] for i in idx)
        boots_g.append(g / len(idx))
        boots_r.append(g / c if c else 0.0)
    boots_g.sort(); boots_r.sort()
    q = lambda xs, p: xs[min(len(xs) - 1, int(p * len(xs)))]
    g = st.mean(gain)
    print(f"gain per state {g:+.4f} [{q(boots_g, .025):+.4f}, {q(boots_g, .975):+.4f}]; on the plateau "
          f"{g * len(states) / a.n_states:+.4f} [{q(boots_g, .025) * len(states) / a.n_states:+.4f}, "
          f"{q(boots_g, .975) * len(states) / a.n_states:+.4f}]; {sum(x > 0.01 for x in gain)} states gained > 0.01")
    r = sum(gain) / sum(calls) if sum(calls) else 0.0
    p = sum(x > a.width_per_call for x in boots_r) / len(boots_r)
    print(f"gain per extra call {r:.5f} [{q(boots_r, .025):.5f}, {q(boots_r, .975):.5f}] against one more chain "
          f"{a.width_per_call:.5f}: P(better) {p:.2f} -> {'adopt' if p >= 0.9 else 'not adopted'} by the costly rule")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

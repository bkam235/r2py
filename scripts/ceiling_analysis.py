"""Capability ceiling (test `glm53-ceiling`, registered 2026-11-08): the default with its agent on GLM 5.3 against the
default with Gemma, on the same 60 frozen training starts, both scored under the same scorer.

Inputs: the ceiling run's results.jsonl (strata, calls, usage) and two re-verifications of final programs
(`scripts/reverify_finals.py`): the baseline (default, e8 sample 0) and the ceiling run (sample 0).

Primary: mean final, ceiling minus baseline, paired by state, 95% bootstrap interval over states (descriptive).
Secondary: by start stratum; states better / worse / tied; finals >= 0.9; among the entities the baseline final
loses (< 0.9), the share the ceiling final scores >= 0.9; the ceiling run's calls and cost per model.

    python scripts/ceiling_analysis.py work/ceiling_glm53/results.jsonl \\
        work/ceiling_glm53/baseline_default_e8_s0_epoch9.jsonl work/ceiling_glm53/finals_epoch9.jsonl
"""
import json
import random
import statistics as st
import sys
from collections import Counter
from pathlib import Path


def load(p):
    return {r["stem"]: r for r in map(json.loads, open(p, encoding="utf-8")) if "ents" in r}


def ci(xs, n=10000, seed=1):
    rng = random.Random(seed)
    means = sorted(st.mean(rng.choices(xs, k=len(xs))) for _ in range(n))
    return means[int(0.025 * n)], means[int(0.975 * n)]


def main(results, base_path, ceil_path):
    rows = {Path(r["script"]).stem: r for r in map(json.loads, open(results, encoding="utf-8"))
            if "final_score" in r and not r.get("invalid")}
    base, ceil = load(base_path), load(ceil_path)
    states = sorted(set(rows) & set(base) & set(ceil))
    print(f"states paired: {len(states)} (ceiling rows {len(rows)}, baseline {len(base)}, ceiling finals {len(ceil)})")
    for name, sel in (("all", states), ("running starts", [s for s in states if rows[s]["start_exit"] == 0]),
                      ("crashing starts", [s for s in states if rows[s]["start_exit"] != 0])):
        if not sel:
            continue
        d = [ceil[s]["aggregate"] - base[s]["aggregate"] for s in sel]
        lo, hi = ci(d)
        print(f"{name:16s} n={len(sel):2d}  baseline {st.mean(base[s]['aggregate'] for s in sel):.3f}  "
              f"ceiling {st.mean(ceil[s]['aggregate'] for s in sel):.3f}  diff {st.mean(d):+.3f} [{lo:+.3f}, {hi:+.3f}]  "
              f"better {sum(x > 0.005 for x in d)} / worse {sum(x < -0.005 for x in d)} / tied {sum(abs(x) <= 0.005 for x in d)}")
    print(f"finals >= 0.9: baseline {sum(base[s]['aggregate'] >= 0.9 for s in states)}, "
          f"ceiling {sum(ceil[s]['aggregate'] >= 0.9 for s in states)} of {len(states)}")
    lost = solved = 0
    for s in states:
        for e, v in base[s]["ents"].items():
            if v["score"] < 0.9:
                lost += 1
                solved += (ceil[s]["ents"].get(e, {}).get("score", 0) >= 0.9)
    print(f"entities the baseline final loses (< 0.9): {lost}; the ceiling final scores >= 0.9 on {solved} "
          f"({solved / lost:.0%})" if lost else "no losing entities")
    calls, usage = Counter(), {}
    for r in rows.values():
        calls["agent steps"] += r.get("llm_steps", 0)
        for m, u in (r.get("usage") or {}).items():
            usage.setdefault(m, Counter()).update(u)
    print("calls:", dict(calls))
    for m, u in usage.items():
        print(f"  {m}: calls {u['calls']}, input {u['prompt_tokens']:,}, output {u['completion_tokens']:,} "
              f"(reasoning {u['reasoning_tokens']:,}), cost ${u['cost']:.2f}")
    print("largest moves:")
    for s in sorted(states, key=lambda s: -abs(ceil[s]["aggregate"] - base[s]["aggregate"]))[:12]:
        print(f"  {s:50s} {base[s]['aggregate']:.3f} -> {ceil[s]['aggregate']:.3f}")


if __name__ == "__main__":
    main(*sys.argv[1:4])

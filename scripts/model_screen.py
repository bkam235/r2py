"""Model screen at the stall-2 step (test `model-screen-stall2`, registered 2026-11-08): the 235 saved chains of
`free-probe-stall2` continued at their stall-2 point with free probes evaluated in the script's own R state
(`probe_state`), once with the agent on Gemma (`stall2_ps`) and once per cheap model (`stall2_ps_<tag>`, pinned
provider, reasoning capped at 8k, output limit 36k; glmflash on novita/fp8, gptoss on deepinfra/bf16, dsflash on
deepinfra/fp8). The anti-hardcoding review stays on Gemma in every arm.

Analysis, per arm against the Gemma arm `stall2_ps`, as in `scripts/stall2_continue.py`: each run's final is
recomputed with the continued chains in place of what they did after their stall-2 point; per state (mean over its
runs) gain = final(arm) - final(stall2_ps); bootstrap over states of the gain on the plateau (sum / 60), P(gain > 0).
Descriptive also: chains improved, probes per chain, "done"s, calls, cost per chain (all models in the arm).
Reference rows: `stall2_default` and `stall2_fp` from `work/stall2_continue`.

    python scripts/model_screen.py run --workers 6 --budget 10 [--arms stall2_ps_gptoss] [--limit 2 --out work/x]
    python scripts/model_screen.py analyze
"""
from __future__ import annotations

import argparse
import collections
import json
import random
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import stall2_continue as s2  # noqa: E402

OUT = ROOT / "work/model_screen"
REF = "stall2_ps"
# stall2_ps_qwenflash is defined but not run: its only provider (alibaba) is excluded by the account's
# zero-data-retention setting, and every call failed in the smoke.
ARMS = (REF, "stall2_ps_glmflash", "stall2_ps_gptoss", "stall2_ps_dsflash")


def _rows(path: Path) -> dict:
    if not path.exists():
        return {}
    out = {}
    for r in map(json.loads, path.open(encoding="utf-8")):
        if "final_score" not in r or r.get("invalid"):
            continue
        # A blocked or failing agent model leaves an ordinary-looking row with no calls of that model: not valid.
        # A start at or above the threshold (0.9) needs no call and is valid.
        if (r.get("agent_model") and r["agent_model"].removeprefix("openrouter:") not in (r.get("usage") or {})
                and float(r["start_score"]) < 0.9):
            print(f"  invalid (no {r['agent_model']} calls): {r['script']} {r['policy']} {r['sample']}")
            continue
        out[(r["script"], r["policy"], r["sample"])] = r
    return out


def finals(ch: dict, rows: dict, arm: str) -> dict:
    """script -> mean over its runs of the run's final with this arm's continuations substituted; None if any of
    the state's continuations is missing."""
    runs = collections.defaultdict(dict)
    for (script, run_label, b), c in ch.items():
        runs[(script, run_label)][b] = c
    out = collections.defaultdict(list)
    for (script, run_label), bs in runs.items():
        best = max(c["start"] for c in bs.values())
        for b, c in bs.items():
            if c["reached"]:
                r = rows.get((script, arm, f"{run_label}.{b}"))
                if r is None:
                    out[script].append(None)
                    break
                best = max(best, float(r["final_score"]), c["score"])
            else:
                best = max(best, c["best"])
        else:
            out[script].append(best)
    return {s: (None if None in v else st.mean(v)) for s, v in out.items()}


def describe(arm: str, rs: list) -> str:
    acts, cost = collections.Counter(), 0.0
    for r in rs:
        acts.update(r["agent"]["action"])
        cost += sum(u["cost"] for u in (r.get("usage") or {}).values())
    probes = sum(r["agent"]["outcome"].get("probe_r:free", 0) for r in rs)
    return (f"{arm:20s} chains {len(rs):3d}  improved {sum(str(r['improved']) == 'True' for r in rs):3d}  "
            f"mean gain {st.mean(float(r['final_score']) - float(r['start_score']) for r in rs):+.4f}  "
            f"calls {sum(int(r['llm_steps']) for r in rs):4d}  free probes {probes:3d} ({probes / len(rs):.2f}/chain)  "
            f"done {acts.get('done', 0):2d}  cost ${cost:.2f} (${cost / len(rs):.4f}/chain)")


def analyze() -> None:
    ch = s2.chains()
    rows = {**_rows(s2.OUT / "results.jsonl"), **_rows(OUT / "results.jsonl")}
    by_arm = collections.defaultdict(list)
    for (_, arm, _), r in rows.items():
        by_arm[arm].append(r)
    print("arms (all chains each arm finished):")
    for arm in ("stall2_default", "stall2_fp", *ARMS):
        if by_arm.get(arm):
            print("  " + describe(arm, by_arm[arm]))
    ref = finals(ch, rows, REF)
    for arm in ARMS[1:]:
        f = finals(ch, rows, arm)
        states = sorted(s for s in ref if ref[s] is not None and f.get(s) is not None)
        if not states:
            continue
        g = {s: f[s] - ref[s] for s in states}
        rng = random.Random(0)
        boots = sorted(sum(g[rng.choice(states)] for _ in states) / 60 for _ in range(10000))
        print(f"{arm:20s} vs {REF}: states {len(states)}, gain on the plateau {sum(g.values()) / 60:+.4f} "
              f"[{boots[250]:+.4f}, {boots[9749]:+.4f}]  P(gain > 0) {sum(b > 0 for b in boots) / len(boots):.2f}  "
              f"better {sum(v > 0.005 for v in g.values())} / worse {sum(v < -0.005 for v in g.values())}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "analyze"])
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--budget", type=float, default=10.0)
    ap.add_argument("--reserve", type=float, default=0.5)
    ap.add_argument("--arms", nargs="+", default=list(ARMS))
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    if a.cmd == "run":
        s2.run(a.workers, a.budget, a.reserve, arms=a.arms, out_dir=Path(a.out), limit=a.limit)
    else:
        analyze()

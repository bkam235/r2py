"""Compare two smoke-test arms (same scripts, same library) from their rows.

    python scripts/compare_arms.py work/smoke/<X> work/smoke/<Y> [--noise work/smoke/<A> work/smoke/<B>]

``--noise`` takes two arms that differ in nothing that matters (the replace_entity on/off pair
is one: the model never used the option).  Their paired differences measure the run-to-run
noise, and the smallest effect this design can detect follows from it.

Prints: paired score difference, the scripts that swing, rewrite outcomes per action, stop reasons.
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import statistics as st
from collections import Counter
from pathlib import Path

SCORED = ("improved", "unchanged", "worse", "catastrophic")


def load(directory: str) -> dict[str, dict]:
    rows = {}
    for f in sorted(glob.glob(str(Path(directory) / "rows*.jsonl"))):
        for line in Path(f).read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                rows[r["script"]] = r
    return rows


def paired(x: dict, y: dict) -> tuple[list[str], list[float], list[float]]:
    scripts = sorted(s for s in set(x) & set(y) if "score" in x[s] and "score" in y[s])
    return scripts, [x[s]["score"] for s in scripts], [y[s]["score"] for s in scripts]


def diff_stats(a: list[float], b: list[float]) -> dict:
    d = [q - p for p, q in zip(a, b)]
    out = {"n": len(d), "mean_a": st.mean(a), "mean_b": st.mean(b), "diff": st.mean(d),
           "sd": st.stdev(d) if len(d) > 1 else float("nan"), "ties": sum(abs(v) < 1e-9 for v in d)}
    out["se"] = out["sd"] / math.sqrt(len(d))
    try:
        from scipy.stats import wilcoxon
        out["p"] = float(wilcoxon(d).pvalue) if any(abs(v) > 1e-9 for v in d) else 1.0
    except ImportError:
        out["p"] = float("nan")
    return out


def outcomes(rows: dict[str, dict]) -> tuple[dict[str, Counter], Counter, Counter]:
    by_action: dict[str, Counter] = {}
    stops: Counter = Counter()
    actions: Counter = Counter()
    for r in rows.values():
        a = r.get("agent") or {}
        actions.update(a.get("action", {}))
        stops.update(a.get("stop", {}))
        for key, n in (a.get("outcome") or {}).items():
            action, kind = key.split(":", 1)
            by_action.setdefault(action, Counter())[kind] += n
    return by_action, stops, actions


def outcome_lines(rows: dict[str, dict], label: str) -> list[str]:
    by_action, stops, actions = outcomes(rows)
    lines = [f"{label}: actions {dict(actions)}  stops {dict(stops)}"]
    for action, c in sorted(by_action.items()):
        n = sum(c[k] for k in SCORED)
        share = " ".join(f"{k} {c[k] / n:.0%}" for k in SCORED) if n else "(none scored)"
        other = ", ".join(f"{k} {v}" for k, v in sorted(c.items()) if k not in SCORED)
        lines.append(f"   {action:14s} n={n:3d}  {share}" + (f"  | {other}" if other else ""))
    return lines


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("x")
    ap.add_argument("y")
    ap.add_argument("--noise", nargs=2, metavar=("A", "B"), help="a replicate pair, for the noise floor")
    args = ap.parse_args()

    X, Y = load(args.x), load(args.y)
    scripts, a, b = paired(X, Y)
    s = diff_stats(a, b)
    print(f"{len(scripts)} scripts in both arms ({len(X)} / {len(Y)} in each)")
    print(f"mean  X {s['mean_a']:.3f}   Y {s['mean_b']:.3f}   diff (Y-X) {s['diff']:+.3f}   "
          f"SE {s['se']:.3f}   SD of diffs {s['sd']:.3f}   exact ties {s['ties']}/{s['n']}   Wilcoxon p={s['p']:.3f}")
    print(f"reach >= 0.9:  X {sum(v >= 0.9 for v in a)}   Y {sum(v >= 0.9 for v in b)}")

    if args.noise:
        ns, na, nb = paired(load(args.noise[0]), load(args.noise[1]))
        n = diff_stats(na, nb)
        mde = 2.8 * n["sd"] / math.sqrt(len(scripts))
        print(f"noise floor from the replicate pair: SD of diffs {n['sd']:.3f} (n={n['n']}); "
              f"smallest detectable mean difference at {len(scripts)} scripts ~ {mde:.3f}")
        flag = "within" if abs(s["diff"]) < mde else "OUTSIDE"
        print(f"the observed difference {s['diff']:+.3f} is {flag} that noise band")

    print("\nscripts that swing by more than 0.25:")
    for sc, p, q in zip(scripts, a, b):
        if abs(q - p) > 0.25:
            print(f"   {sc[:55]:55s} X {p:.2f} -> Y {q:.2f}")

    print()
    for line in outcome_lines(X, "X") + outcome_lines(Y, "Y"):
        print(line)
    print("\n(rates at n~70 carry about +-10 points of noise: smaller differences cannot be attributed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

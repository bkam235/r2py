"""Idea 4, diagnose then fix: one step, U (production, 1 call) vs D (diagnosis, then fix: 2 calls). Registered 2026-10-20.

`step_ab.py run --tag diag --with-crashing --arms U D --samples 2`. Primary: P(the step improves), D - U, paired per
state (mean over samples), bootstrap over states. Secondary: D against the best of U's 2 samples (the same number of
calls), realized gain, running and crashing starts apart.

    python scripts/diagnose_test.py
"""
import json
import random
import statistics as st
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def ci(d, rng):
    b = sorted(st.mean(rng.choice(d) for _ in d) for _ in range(5000))
    return f"{st.mean(d):+.4f} [{b[125]:+.4f}, {b[4874]:+.4f}]  ({len(d)} states)"


def main() -> None:
    rows = [json.loads(l) for l in (ROOT / "work/step_ab_diag/results.jsonl").open(encoding="utf-8")]
    rows = [r for r in rows if r.get("outcome") != "provider_unavailable"]
    print(f"{len(rows)} steps, errors {sum(str(r.get('outcome', '')).startswith('error') for r in rows)}")
    per = defaultdict(lambda: defaultdict(list))
    crashing = {}
    for r in rows:
        per[r["arm"]][r["script"]].append(r)
        if "exit_before" in r:
            crashing[r["script"]] = r["exit_before"] != 0
    imp = lambda r: float(bool(r.get("improved")))   # noqa: E731
    rng = random.Random(0)
    for label, sel in (("all", lambda s: True), ("running starts", lambda s: not crashing.get(s, False)),
                       ("crashing starts", lambda s: crashing.get(s, False))):
        ks = [s for s in per["U"] if s in per["D"] and sel(s)]
        if not ks:
            continue
        print(f"\n{label}:")
        for arm in ("U", "D"):
            rs = [r for s in ks for r in per[arm][s]]
            print(f"  {arm}: steps {len(rs)}  P(improve) {st.mean(map(imp, rs)):.3f}  "
                  f"realized gain {st.mean(r.get('gain', 0) for r in rs):+.4f}")
        print(f"  U best of 2: P(improve) {st.mean(max(map(imp, per['U'][s])) for s in ks):.3f}")
        print("  D - U, P(improve):", ci([st.mean(map(imp, per['D'][s])) - st.mean(map(imp, per['U'][s])) for s in ks], rng))
        print("  D - U, realized gain:", ci([st.mean(r.get('gain', 0) for r in per['D'][s]) - st.mean(r.get('gain', 0) for r in per['U'][s]) for s in ks], rng))
        print("  D - U best of 2, P(improve):", ci([st.mean(map(imp, per['D'][s])) - max(map(imp, per['U'][s])) for s in ks], rng))


if __name__ == "__main__":
    main()

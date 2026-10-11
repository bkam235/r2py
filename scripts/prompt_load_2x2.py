"""Analysis of the registered 2x2 follow-up (system prompt x content), work/prompt_load_sys2x2/."""
import json
import random
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CELLS = {("agent", "full"): "A2_full_entity", ("short", "local"): "A5_local",
         ("short", "full"): "B1_full_entity_shortsys", ("agent", "local"): "B2_local_agentsys"}


def main() -> int:
    rows = [json.loads(l) for l in (ROOT / "work/prompt_load_sys2x2/results.jsonl").open(encoding="utf-8")]
    rows = [r for r in rows if r.get("outcome") != "provider_unavailable"]
    print(f"{len(rows)} calls")
    for metric in ("canary_in_entity", "adopted"):
        rate = defaultdict(list)                     # (case, arm) -> outcomes
        for r in rows:
            rate[((r["script"], r["entity"]), r["arm"])].append(bool(r.get(metric)))
        cases = sorted({k[0] for k in rate})

        def cell(case, s, c):
            v = rate.get((case, CELLS[(s, c)]), [])
            return sum(v) / len(v) if v else 0.0

        def effects(cs):
            sys_eff = st.mean((cell(k, "short", c) - cell(k, "agent", c)) for k in cs for c in ("full", "local"))
            con_eff = st.mean((cell(k, s, "local") - cell(k, s, "full")) for k in cs for s in ("agent", "short"))
            return sys_eff, con_eff
        point = effects(cases)
        rng = random.Random(0)
        boots = [effects([rng.choice(cases) for _ in cases]) for _ in range(5000)]
        print(f"\n{metric}:")
        for (s, c), arm in CELLS.items():
            print(f"  {s:<6}system  {c:<6}content  {st.mean(cell(k, s, c) for k in cases):6.1%}")
        for i, name in enumerate(("system (short - agent)", "content (local - full)")):
            lo, hi = sorted(b[i] for b in boots)[125], sorted(b[i] for b in boots)[4874]
            verdict = "MATTERS" if abs(point[i]) >= 0.10 and (lo > 0 or hi < 0) else "does not meet the rule"
            print(f"  {name:<24}{point[i]:+.1%}  95% [{lo:+.1%}, {hi:+.1%}]  {verdict}")
    d = defaultdict(list)
    for r in rows:
        if r.get("outcome") == "verified":
            d[r["arm"]].append((r["after"] or 0) - r["before"])
    print("\nentity score change:", {a: round(st.mean(v), 3) for a, v in d.items()})
    return 0


if __name__ == "__main__":
    sys.exit(main())

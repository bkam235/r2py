"""Compare concurrent replay arms against a baseline, paired per state, reported by start stratum (2026-10-16).

Every recent loop effect (S1 +0.017, locator +0.029, crash-first -0.019) came with an interval of about +-0.06,
and half of the dev states' noise is crash-or-not. So: arms run concurrently (a day-apart baseline drifted by
0.01-0.02 on states the treatment never touched), the state is the unit (mean over samples), and states whose
start crashes are reported apart from states whose start runs.

    python scripts/replay_compare.py work/replay_x/results.jsonl --baseline rewrite_w3
"""
from __future__ import annotations

import argparse
import json
import random
import statistics as st
from collections import defaultdict


def compare(rows: list[dict], baseline: str) -> str:
    rows = [r for r in rows if "final_score" in r]
    per = defaultdict(lambda: defaultdict(list))
    start_crashes = {}
    for r in rows:
        per[r["policy"]][r["script"]].append(r)
        start_crashes[r["script"]] = r.get("start_exit", 0) != 0
    lines = []
    for pol, by in sorted(per.items()):
        rs = [r for v in by.values() for r in v]
        lines.append(f"{pol:<22} runs {len(rs):>4}  states {len(by):>3}  mean final {st.mean(r['final_score'] for r in rs):.3f}"
                     f"  P(>=0.9) {st.mean(r['final_score'] >= 0.9 for r in rs):.2f}"
                     f"  ends running {sum(r.get('final_exit') == 0 for r in rs)}/{len(rs)}"
                     f"  steps {st.mean(r.get('llm_steps', 0) for r in rs):.1f}")
    base = per.get(baseline, {})
    for stratum, sel in (("all", lambda s: True), ("running starts", lambda s: not start_crashes[s]),
                         ("crashing starts", lambda s: start_crashes[s])):
        lines.append(f"\n{stratum}:")
        for pol in sorted(p for p in per if p != baseline):
            ks = sorted(k for k in set(per[pol]) & set(base) if sel(k))
            if len(ks) < 2:
                continue
            diff = [st.mean(r["final_score"] for r in per[pol][k]) - st.mean(r["final_score"] for r in base[k])
                    for k in ks]
            rng = random.Random(0)
            boots = sorted(st.mean(rng.choice(diff) for _ in diff) for _ in range(5000))
            nz = [x for x in diff if abs(x) > 1e-9]
            try:
                from scipy.stats import wilcoxon
                p = wilcoxon(nz).pvalue if len(nz) >= 5 else float("nan")
            except ImportError:
                p = float("nan")
            lines.append(f"  {pol} vs {baseline}: {st.mean(diff):+.3f} [{boots[125]:+.3f}, {boots[4874]:+.3f}]  "
                         f"better/worse/tied {sum(x > 0.005 for x in diff)}/{sum(x < -0.005 for x in diff)}/"
                         f"{sum(abs(x) <= 0.005 for x in diff)}  Wilcoxon p {p:.3f}  ({len(ks)} states)")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results")
    ap.add_argument("--baseline", default="rewrite_w3")
    args = ap.parse_args()
    rows = [json.loads(l) for l in open(args.results, encoding="utf-8") if l.strip()]
    print(compare(rows, args.baseline))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Feedback ablation: does one agent step use its verification feedback? (registered 2026-10-19, before the run)

Arms of `step_ab.py run --tag ablation --with-crashing --arms U S N`, identical except for the turn's
"Verification result" section: U full (production), S scores only (aggregate, crash flag, per-entity scores), N none.
Primary: P(the step improves), and realized gain, paired per state (mean over samples), U - N and U - S, 95% bootstrap
interval over states; reported for running and crashing starts apart.

    python scripts/feedback_ablation.py
"""
import json
import random
import statistics as st
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    rows = [json.loads(l) for l in (ROOT / "work/step_ab_ablation/results.jsonl").open(encoding="utf-8")]
    rows = [r for r in rows if r.get("outcome") != "provider_unavailable"]
    errors = sum(str(r.get("outcome", "")).startswith("error") for r in rows)
    print(f"{len(rows)} steps, errors {errors}")
    per = defaultdict(lambda: defaultdict(list))
    crashing = {}
    for r in rows:
        per[r["arm"]][r["script"]].append(r)
        if "exit_before" in r:
            crashing[r["script"]] = r["exit_before"] != 0
    rng = random.Random(0)
    for label, sel in (("all", lambda s: True), ("running starts", lambda s: not crashing[s]), ("crashing starts", lambda s: crashing[s])):
        print(f"\n{label}:")
        for arm in ("U", "S", "N"):
            rs = [r for s, v in per[arm].items() if sel(s) for r in v]
            if rs:
                print(f"  {arm}: steps {len(rs)}  P(improve) {st.mean(bool(r.get('improved')) for r in rs):.3f}  "
                      f"realized gain {st.mean(r.get('gain', 0) for r in rs):+.4f}  runs after {st.mean(r.get('exit_after') == 0 for r in rs if 'exit_after' in r) if any('exit_after' in r for r in rs) else float('nan'):.2f}")
        for other in ("N", "S"):
            for metric, f in (("P(improve)", lambda r: float(bool(r.get("improved")))), ("realized gain", lambda r: r.get("gain", 0))):
                ks = [s for s in per["U"] if s in per[other] and sel(s)]
                d = [st.mean(map(f, per["U"][s])) - st.mean(map(f, per[other][s])) for s in ks]
                if not d:
                    continue
                b = sorted(st.mean(rng.choice(d) for _ in d) for _ in range(5000))
                print(f"  U - {other}, {metric}: {st.mean(d):+.4f} [{b[125]:+.4f}, {b[4874]:+.4f}]  ({len(d)} states)")


if __name__ == "__main__":
    main()

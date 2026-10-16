"""Translation manual, stage 1: analysis of the one-step frozen-design test (registered 2026-10-16).

Arms U (today) and F (helper interfaces frozen and enforced) from `step_ab.py run --tag stage1 --arms U F`.
Stop rule: stop if F improves less often than U (paired over states, 95% interval entirely below 0) AND does not
reduce damage (interval of the damage difference not entirely below 0). Otherwise go on to stage 2.

    python scripts/manual_stage1.py
"""
import json
import random
import statistics as st
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    rows = [json.loads(l) for l in (ROOT / "work/step_ab_stage1/results.jsonl").open(encoding="utf-8")]
    rows = [r for r in rows if r.get("outcome") != "provider_unavailable"]
    print(f"{len(rows)} steps; errors {sum(str(r.get('outcome', '')).startswith('error') for r in rows)}")
    improved = lambda r: float(bool(r.get("improved")))                                        # noqa: E731
    damaged = lambda r: float((r.get("damaged") or 0) > 0)                                    # noqa: E731
    changed = lambda r: float(bool(r.get("interface_changed")))                               # noqa: E731
    per = defaultdict(lambda: defaultdict(list))
    for r in rows:
        per[r["arm"]][r["script"]].append(r)
    for arm in ("U", "F"):
        rs = [r for v in per[arm].values() for r in v]
        v = [r for r in rs if r.get("outcome") == "verified"]
        print(f"{arm}: steps {len(rs)}  P(improve) {st.mean(map(improved, rs)):.3f}  "
              f"realized gain {st.mean(r.get('gain', 0) for r in rs):+.4f}  "
              f"P(damage a verified entity) {st.mean(map(damaged, v)) if v else 0:.3f}  "
              f"mean entities damaged {st.mean(r.get('damaged', 0) for r in v) if v else 0:.2f}  "
              f"attempted interface change {st.mean(map(changed, v)) if v else 0:.3f}  "
              f"restored {sum(bool(r.get('interface_restored')) for r in rs)}  "
              f"no rewrite {sum(r.get('outcome') == 'no rewrite' for r in rs)}  "
              f"gate {sum(r.get('outcome') == 'gate rejected' for r in rs)}  "
              f"review rej {sum(bool(r.get('review_rejected')) for r in rs)}")
    rng = random.Random(0)
    ks = sorted(set(per["F"]) & set(per["U"]))
    res = {}
    for name, f, only_verified in (("P(improve)", improved, False), ("P(damage)", damaged, True),
                                   ("realized gain", lambda r: r.get("gain", 0), False)):
        def m(rs):
            rs = [r for r in rs if r.get("outcome") == "verified"] if only_verified else rs
            return st.mean(map(f, rs)) if rs else None
        pairs = [(m(per["F"][k]), m(per["U"][k])) for k in ks]
        diff = [a - b for a, b in pairs if a is not None and b is not None]
        boots = sorted(st.mean(rng.choice(diff) for _ in diff) for _ in range(5000))
        res[name] = (st.mean(diff), boots[125], boots[4874])
        print(f"F - U, {name}: {st.mean(diff):+.4f} [{boots[125]:+.4f}, {boots[4874]:+.4f}]  ({len(diff)} states)")
    worse_improve = res["P(improve)"][2] < 0
    less_damage = res["P(damage)"][2] < 0
    print("\nDecision:", "STOP (F improves less often and does not reduce damage)" if worse_improve and not less_damage
          else "go on to stage 2 (two-step retention)")


if __name__ == "__main__":
    main()

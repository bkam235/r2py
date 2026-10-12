"""Analyses of Part A (system prompt trimming) and Part B (crash-first replay), as registered 2026-10-12.

    python scripts/parts_ab_analysis.py a
    python scripts/parts_ab_analysis.py b
"""
import json
import random
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARMS = ("S0_current", "S1_minimal", "S2_rules", "S3_no_tools")       # S1 < S2 < S3 < S0 in length
BY_LENGTH = ("S1_minimal", "S2_rules", "S3_no_tools")


def part_a() -> None:
    rows = [json.loads(l) for l in (ROOT / "work/prompt_load_sysprompt/results.jsonl").open(encoding="utf-8")]
    rows = [r for r in rows if r.get("outcome") != "provider_unavailable"]
    print(f"{len(rows)} calls")
    cell = defaultdict(list)
    for r in rows:
        cell[((r["script"], r["entity"]), r["arm"])].append(r)
    cases = sorted({k[0] for k in cell})

    def rate(case, arm, f):
        rs = cell.get((case, arm), [])
        return sum(f(r) for r in rs) / len(rs) if rs else 0.0
    adopted = lambda r: bool(r.get("adopted"))                       # noqa: E731
    violation = lambda r: bool(r.get("syntax_error") or r.get("review_rejected"))   # noqa: E731
    canary = lambda r: bool(r.get("canary_in_entity"))               # noqa: E731
    print(f"{'arm':<14}{'canary':>8}{'adopted':>9}{'violations':>12}{'syntax':>8}{'review rej':>11}"
          f"{'arg fixes':>10}{'d score (unblocked)':>21}")
    for arm in ARMS:
        rs = [r for r in rows if r["arm"] == arm]
        unblocked = [r for r in rs if r.get("outcome") == "verified" and r.get("status_after") != "blocked"]
        print(f"{arm:<14}{st.mean(map(canary, rs)):>8.0%}{st.mean(map(adopted, rs)):>9.0%}"
              f"{st.mean(map(violation, rs)):>12.0%}{st.mean(bool(r.get('syntax_error')) for r in rs):>8.0%}"
              f"{st.mean(bool(r.get('review_rejected')) for r in rs):>11.0%}"
              f"{st.mean(r.get('arg_order_fixes', 0) for r in rs):>10.2f}"
              f"{st.mean((r['after'] or 0) - r['before'] for r in unblocked) if unblocked else 0:>+21.3f}")
    rng = random.Random(0)
    winner = None
    for arm in BY_LENGTH:
        def diff(cs, f):
            return st.mean(rate(c, arm, f) - rate(c, "S0_current", f) for c in cs)
        boots = []
        for _ in range(5000):
            cs = [rng.choice(cases) for _ in cases]
            boots.append((diff(cs, adopted), diff(cs, violation)))
        a, v = diff(cases, adopted), diff(cases, violation)
        lo, hi = sorted(b[0] for b in boots)[125], sorted(b[0] for b in boots)[4874]
        ok = a >= 0.10 and lo > 0 and v <= 0.05
        print(f"{arm} vs S0: adoption {a:+.1%} 95% [{lo:+.1%}, {hi:+.1%}], violations {v:+.1%} -> "
              f"{'QUALIFIES' if ok else 'does not qualify'}")
        if ok and winner is None:
            winner = arm
    print(f"\nDecision: {winner or 'S0_current (no shorter prompt qualifies)'}")


def _first_running_step(path: Path):
    for line in path.open(encoding="utf-8"):
        e = json.loads(line)
        if e["kind"] == "step" and e.get("exit_code") == 0:
            return e["step"]
    return None


def part_b() -> None:
    from scipy.stats import wilcoxon

    def load(d):
        rows = [json.loads(l) for l in (ROOT / d / "results.jsonl").open(encoding="utf-8")]
        rows = [r for r in rows if r.get("policy") == "rewrite_w3" and "final_score" in r]
        for r in rows:
            f = ROOT / d / "trajectories" / f"{Path(r['script']).stem}.rewrite_w3.{r['sample']}.jsonl"
            r["first_running_step"] = _first_running_step(f) if f.exists() else None
        return rows
    new, old = load("work/replay_crashfirst"), load("work/replay_feedback")
    crashing = sorted({r["script"] for r in old if r.get("start_exit", 0) != 0})
    print(f"runs: crash-first {len(new)}, baseline {len(old)}; crashing start states: {len(crashing)}")
    for name, sel in (("crashing starts", lambda r: r["script"] in crashing),
                      ("running starts", lambda r: r["script"] not in crashing)):
        print(f"\n{name}:")
        per = {}
        for arm, rows in (("crash-first", new), ("baseline", old)):
            rs = [r for r in rows if sel(r)]
            steps = [r["first_running_step"] for r in rs if r["first_running_step"] is not None]
            print(f"  {arm:<12} runs {len(rs):>3}  ends running {sum(r.get('final_exit') == 0 for r in rs):>3}"
                  f"  mean final {st.mean(r['final_score'] for r in rs):.3f}"
                  + (f"  first running step: median {st.median(steps)} (reached in {len(steps)})"
                     if name == "crashing starts" else ""))
            d = defaultdict(list)
            for r in rs:
                d[r["script"]].append(r["final_score"])
            per[arm] = {k: st.mean(v) for k, v in d.items()}
        ks = sorted(set(per["crash-first"]) & set(per["baseline"]))
        diff = [per["crash-first"][k] - per["baseline"][k] for k in ks]
        nz = [x for x in diff if abs(x) > 1e-9]
        p = wilcoxon(nz).pvalue if len(nz) >= 5 else float("nan")
        print(f"  paired per state: {st.mean(diff):+.3f}, better/worse/tied "
              f"{sum(x > 0.005 for x in diff)}/{sum(x < -0.005 for x in diff)}/{sum(abs(x) <= 0.005 for x in diff)}, "
              f"Wilcoxon p {p:.3f}")
        if name == "crashing starts":
            for k in ks:
                print(f"    {k[:44]:<46} baseline {per['baseline'][k]:.2f}  crash-first {per['crash-first'][k]:.2f}")


if __name__ == "__main__" and sys.argv[1] in ("a", "b"):
    {"a": part_a, "b": part_b}[sys.argv[1]]()


S1REF = ("S0_current", "S1_minimal", "S1a_follow", "S1b_follow_compute")


def s1ref() -> None:
    """S1 refinement, step 2 (registered 2026-10-12): effects against S0 with 95% bootstrap intervals over cases;
    selection = the S1 variant with the highest adoption whose violation interval does not lie above 0."""
    rows = [json.loads(l) for l in (ROOT / "work/prompt_load_s1ref/results.jsonl").open(encoding="utf-8")]
    rows = [r for r in rows if r.get("outcome") != "provider_unavailable"]
    print(f"{len(rows)} calls")
    cell = defaultdict(list)
    for r in rows:
        cell[((r["script"], r["entity"]), r["arm"])].append(r)
    cases = sorted({k[0] for k in cell})
    adopted = lambda r: float(bool(r.get("adopted")))                                   # noqa: E731
    violation = lambda r: float(bool(r.get("syntax_error") or r.get("review_rejected")))  # noqa: E731
    gain = lambda r: ((r["after"] or 0) - r["before"]) if (r.get("outcome") == "verified"   # noqa: E731
                                                           and r.get("status_after") != "blocked") else 0.0

    def rate(case, arm, f):
        rs = cell.get((case, arm), [])
        return sum(f(r) for r in rs) / len(rs) if rs else 0.0
    for kind in ("all", "print", "value"):
        rs_k = [r for r in rows if kind == "all" or r["kind"] == kind]
        print(f"\n{kind}: {'arm':<20}{'canary':>8}{'adopted':>9}{'violations':>12}{'review rej':>11}"
              f"{'pasted':>8}{'d score':>9}")
        for arm in S1REF:
            rs = [r for r in rs_k if r["arm"] == arm]
            if rs:
                print(f"      {arm:<20}{st.mean(bool(r.get('canary_in_entity')) for r in rs):>8.0%}"
                      f"{st.mean(map(adopted, rs)):>9.0%}{st.mean(map(violation, rs)):>12.0%}"
                      f"{st.mean(bool(r.get('review_rejected')) for r in rs):>11.0%}"
                      f"{st.mean(bool(r.get('pasted_literal')) for r in rs):>8.0%}{st.mean(map(gain, rs)):>+9.3f}")
    rng = random.Random(0)
    print()
    best = None
    for arm in S1REF[1:]:
        effects = []
        for f in (adopted, violation, gain):
            def d(cs):
                return st.mean(rate(c, arm, f) - rate(c, "S0_current", f) for c in cs)
            boots = sorted(d([rng.choice(cases) for _ in cases]) for _ in range(5000))
            effects.append((d(cases), boots[125], boots[4874]))
        (a, alo, ahi), (v, vlo, vhi), (g, glo, ghi) = effects
        print(f"{arm} vs S0: adoption {a:+.1%} [{alo:+.1%}, {ahi:+.1%}]  violations {v:+.1%} [{vlo:+.1%}, {vhi:+.1%}]"
              f"  score {g:+.3f} [{glo:+.3f}, {ghi:+.3f}]")
        if vlo <= 0 and (best is None or a > best[1]):
            best = (arm, a)
    print(f"\nSelected for step 3: {best[0] if best else 'none (every variant raises violations)'}")


if __name__ == "__main__" and sys.argv[1] == "s1ref":
    s1ref()

"""Experiment kit for the meta-loop (2026-10-24): run guard, common result format, generic analysis.

Run guard (`RunGuard`), used by replay.py, step_ab.py and two_step.py:
  - records the OpenRouter balance at the start and polls it; asks the instrument to stop cleanly once the run has
    spent its budget or the remaining balance falls below a reserve (the in-flight-budget refusals of October
    happened near zero balance and each cost a run);
  - detects wall-clock gaps (a sleeping laptop: the agent's time limit is wall-clock, so a run that overlapped a gap
    was cut short) and marks such rows `invalid: "sleep"`, so the instrument reruns them on resume;
  - writes <out>/run_manifest.json: command, start and end, scorer version, balance and cost, gaps, stop reason.

Common format (`load`): every instrument's rows as {state, arm, sample, stratum, improved, gain, final, invalid}.

Analysis (`analyze`), one command for every experiment:
    python scripts/expkit.py analyze work/step_ab_diag/results.jsonl --baseline U
    python scripts/expkit.py analyze work/two_step/results.jsonl --baseline fresh --metric improved
    python scripts/expkit.py analyze work/replay_k3/results.jsonl --baseline rewrite_w3 --metric final
  per arm: mean of the metric; per arm against the baseline, paired by state (mean over samples): mean difference,
  95% and 90% bootstrap intervals over states, P(difference > 0), better/worse/tied; for all, running and crashing
  starts. `--rule free` or `--rule costly --best-of K` adds the tiered decision rule's verdict.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import statistics as st
import sys
import threading
import time
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------------------------------------- run guard

def credits() -> "tuple[float, float] | None":
    """(total credits, total usage) in USD from OpenRouter, or None if it cannot be read."""
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env", override=True)
        req = urllib.request.Request("https://openrouter.ai/api/v1/credits",
                                     headers={"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"]})
        d = json.load(urllib.request.urlopen(req, timeout=20))["data"]
        return float(d["total_credits"]), float(d["total_usage"])
    except Exception:
        return None


class RunGuard:
    """Budget, reserve and sleep guard around one instrument run (see the module docstring)."""

    GAP_S = 300          # a tick that arrives this much late means the machine was not running

    def __init__(self, out_dir, budget: "float | None" = None, reserve: float = 0.5, poll_s: float = 60,
                 tick_s: float = 10, read_credits=credits):
        self.out_dir, self.budget, self.reserve = Path(out_dir), budget, reserve
        self.poll_s, self.tick_s, self._credits = poll_s, tick_s, read_credits
        self.gaps: list[tuple[float, float]] = []
        self.stop_reason: "str | None" = None
        self.rows = 0
        self._halt = threading.Event()

    def __enter__(self):
        from r2py.scoring import scoring_version
        self.started = time.time()
        self.version = scoring_version()
        c = self._credits()
        self.balance_start = c
        self._thread = threading.Thread(target=self._watch, daemon=True)
        self._thread.start()
        return self

    def _watch(self) -> None:
        last_tick, last_poll = time.time(), 0.0
        while not self._halt.wait(self.tick_s):
            now = time.time()
            if now - last_tick > self.GAP_S:
                self.gaps.append((last_tick, now))
            last_tick = now
            if now - last_poll >= self.poll_s:
                last_poll = now
                self._check_money()

    def _check_money(self) -> None:
        c = self._credits()
        if c is None or self.balance_start is None:
            return
        total, used = c
        spent = used - self.balance_start[1]
        if self.budget is not None and spent >= self.budget:
            self.stop_reason = self.stop_reason or f"budget reached: ${spent:.2f} of ${self.budget:.2f}"
        elif total - used <= self.reserve:
            self.stop_reason = self.stop_reason or f"balance at the reserve: ${total - used:.2f} left"

    def should_stop(self) -> bool:
        return self.stop_reason is not None

    def annotate(self, row: dict) -> dict:
        """Stamp the scorer version; mark a row whose run overlapped a wall-clock gap as invalid."""
        self.rows += 1
        row.setdefault("scoring_version", self.version)
        end = time.time()
        start = end - float(row.get("seconds", 0) or 0)
        if any(g0 < end and g1 > start for g0, g1 in self.gaps):
            row["invalid"] = "sleep"
        return row

    def __exit__(self, *exc):
        self._halt.set()
        self._thread.join(timeout=5)
        end = self._credits()
        b0 = self.balance_start
        manifest = {
            "command": " ".join(sys.argv), "started": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.started)),
            "ended": time.strftime("%Y-%m-%d %H:%M:%S"), "scoring_version": self.version, "rows": self.rows,
            "balance_start": None if b0 is None else round(b0[0] - b0[1], 2),
            "balance_end": None if end is None else round(end[0] - end[1], 2),
            "cost": None if (b0 is None or end is None) else round(end[1] - b0[1], 2),
            "budget": self.budget, "stop_reason": self.stop_reason or ("error" if exc[0] else "finished"),
            "sleep_gaps": [[time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(a)),
                            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(b))] for a, b in self.gaps]}
        self.out_dir.mkdir(parents=True, exist_ok=True)
        f = self.out_dir / "run_manifest.json"
        runs = json.loads(f.read_text(encoding="utf-8")) if f.exists() else []
        runs.append(manifest)
        f.write_text(json.dumps(runs, indent=1), encoding="utf-8")
        print(f"[guard] {manifest['stop_reason']}; cost ${manifest['cost']}; sleep gaps {len(self.gaps)}", flush=True)
        return False


def add_guard_args(p) -> None:
    p.add_argument("--budget", type=float, default=None, help="stop cleanly once the run has spent this many USD")
    p.add_argument("--reserve", type=float, default=0.5, help="stop cleanly when the balance falls to this (USD)")


# ---------------------------------------------------------------------------------------------- common format

def load(path) -> list[dict]:
    """Rows of any instrument in the common long format."""
    raw = [json.loads(line) for line in Path(path).open(encoding="utf-8")]
    out = []
    for r in raw:
        base = {"state": r.get("script"), "sample": r.get("sample"), "invalid": r.get("invalid")
                or ("error" if ("error" in r or str(r.get("outcome", "")).startswith("error")
                                or r.get("outcome") == "provider_unavailable") else None),
                "scoring_version": r.get("scoring_version")}
        if "fresh_improved" in r:              # two_step.py: two arms in one row
            if not r.get("step2_ran", True):
                continue
            for arm in ("fresh", "conv"):
                imp = bool(r.get(f"{arm}_improved"))
                out.append(dict(base, arm=arm, stratum=_stratum(r, "start_exit"), improved=imp,
                                gain=(max(0.0, r[arm] - r["best1"]) if imp else 0.0) if arm in r else None,
                                final=r.get(arm)))
        elif "arm" in r:                        # step_ab.py
            out.append(dict(base, arm=r["arm"], stratum=_stratum(r, "exit_before"),
                            improved=bool(r.get("improved")), gain=r.get("gain", 0.0), final=r.get("after")))
        elif "policy" in r:                     # replay.py and the continuation scripts
            out.append(dict(base, arm=r["policy"], stratum=_stratum(r, "start_exit"),
                            improved=bool(r.get("improved")),
                            gain=(r["final_score"] - r["start_score"]) if "final_score" in r else None,
                            final=r.get("final_score")))
    # A state belongs to one stratum: some starts crash in one run and run in another (random output), so the
    # stratum is the majority over the state's rows, ties counted as crashing.
    votes = defaultdict(list)
    for r in out:
        if r["stratum"] is not None:          # a row that failed before its start was verified does not vote
            votes[r["state"]].append(r["stratum"] == "crashing")
    for r in out:
        v = votes[r["state"]]
        r["stratum"] = "crashing" if v and 2 * sum(v) >= len(v) else "running"
    return out


def _stratum(r: dict, key: str) -> "str | None":
    return None if key not in r else ("crashing" if r[key] else "running")


# ---------------------------------------------------------------------------------------------- analysis

def _boot(d: list[float], rng, n=10000) -> list[float]:
    return sorted(st.mean(rng.choice(d) for _ in d) for _ in range(n))


def compare_arms(rows, arm, baseline, metric, best_of=1, rng=None):
    """Paired by state: arm - baseline (baseline as the best of `best_of` of its samples when > 1)."""
    rng = rng or random.Random(0)
    val = (lambda r: float(r["improved"])) if metric == "improved" else (lambda r: r[metric])
    by = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r[metric] is not None:
            by[r["arm"]][r["state"]].append(val(r))
    ks = sorted(set(by[arm]) & set(by[baseline]))
    if not ks:
        return None
    def base_value(v):
        if best_of <= 1:
            return st.mean(v)
        import itertools
        return st.mean(max(c) for c in itertools.combinations(v, min(best_of, len(v))))
    d = [st.mean(by[arm][s]) - base_value(by[baseline][s]) for s in ks]
    b = _boot(d, rng)
    n = len(b)
    return {"n_states": len(d), "mean": st.mean(d), "ci95": (b[int(n * .025)], b[int(n * .975) - 1]),
            "ci90": (b[int(n * .05)], b[int(n * .95) - 1]), "p_gt0": sum(x > 0 for x in b) / n,
            "better": sum(x > 1e-9 for x in d), "worse": sum(x < -1e-9 for x in d), "tied": sum(abs(x) <= 1e-9 for x in d)}


def analyze(path, baseline: str, metric: str = "improved", rule: "str | None" = None, best_of: int = 1) -> str:
    rows = load(path)
    invalid = [r for r in rows if r["invalid"]]
    rows = [r for r in rows if not r["invalid"]]
    versions = sorted({r["scoring_version"] for r in rows if r["scoring_version"]})
    arms = sorted({r["arm"] for r in rows})
    lines = [f"{path}: {len(rows)} valid rows, {len(invalid)} invalid "
             f"({', '.join(sorted({r['invalid'] for r in invalid})) or '-'}); arms {arms}; metric {metric}"]
    if len(versions) > 1:
        lines.append(f"WARNING: rows from {len(versions)} scoring versions: {versions}; scores across them do not compare")
    for label, sel in (("all", lambda r: True), ("running starts", lambda r: r["stratum"] == "running"),
                       ("crashing starts", lambda r: r["stratum"] == "crashing")):
        rs = [r for r in rows if sel(r)]
        if not rs:
            continue
        lines.append(f"\n{label}:")
        for arm in arms:
            v = [float(r["improved"]) if metric == "improved" else r[metric] for r in rs if r["arm"] == arm and r[metric] is not None]
            if v:
                lines.append(f"  {arm}: {len(v)} rows, mean {metric} {st.mean(v):.4f}")
        for arm in arms:
            if arm == baseline:
                continue
            c = compare_arms(rs, arm, baseline, metric, best_of=best_of if rule == "costly" else 1)
            if c is None:
                continue
            ref = baseline if not (rule == "costly" and best_of > 1) else f"best of {best_of} {baseline}"
            lines.append(f"  {arm} - {ref}: {c['mean']:+.4f}  95% [{c['ci95'][0]:+.4f}, {c['ci95'][1]:+.4f}]  "
                         f"90% [{c['ci90'][0]:+.4f}, {c['ci90'][1]:+.4f}]  P(>0) {c['p_gt0']:.2f}  "
                         f"better/worse/tied {c['better']}/{c['worse']}/{c['tied']}  ({c['n_states']} states)")
            if rule and label == "all":
                verdict = "ADOPT" if c["p_gt0"] >= 0.9 else "do not adopt"
                lines.append(f"    tiered rule ({rule}{', against best of ' + str(best_of) if rule == 'costly' else ''}): "
                             f"{verdict} (P(>0) {c['p_gt0']:.2f}; also check that no stratum is harmed)")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analyze")
    a.add_argument("results")
    a.add_argument("--baseline", required=True)
    a.add_argument("--metric", choices=["improved", "gain", "final"], default="improved")
    a.add_argument("--rule", choices=["free", "costly"], default=None)
    a.add_argument("--best-of", type=int, default=1, help="with --rule costly: compare with the best of K baseline samples")
    args = ap.parse_args()
    print(analyze(args.results, args.baseline, args.metric, args.rule, args.best_of))
    return 0


if __name__ == "__main__":
    sys.exit(main())

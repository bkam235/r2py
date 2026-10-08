"""Propose verified Python implementations from Rd-harvested cases.

`scripts/rd_harvest.py` records the real calls a package's own `\\examples` block makes, with the
arguments as evaluated at the call site and R's answer. This hands those to `propose.attempt` as
mined cases -- the first test of whether the pilot's 22% pass rate on package functions was a
case-quality artifact (half of attempts never got three valid cases) or a limit of the model.

    python scripts/rd_pilot.py --min-cases 3 --workers 4
    python scripts/rd_pilot.py --summary-only
"""
from __future__ import annotations

import argparse
import json
import multiprocessing
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

HARVEST = ROOT / "work" / "rd_harvest" / "rows.jsonl"
OUT = ROOT / "work" / "runtime" / "rd_pilot"


def as_mined(row: dict) -> list[dict]:
    """Harvested calls in the shape `difftest.run_python` and `propose` expect of mined cases."""
    cases = []
    for c in row.get("cases") or []:
        if c.get("value") is None:
            continue
        cases.append({
            "call": (c.get("call") or f"{row['function']}(...)") + "   [from the package's own examples]",
            "args": c["args"],
            "expected": c["value"],
            "rclass": c.get("rclass") or "",
            "shown": c.get("shown") or "",
            "mined": True,
            "core": True,
            "draws": [],
        })
    # the same arguments twice teaches nothing, and the budget is per function
    seen, out = set(), []
    for c in cases:
        k = json.dumps(c["args"], sort_keys=True)
        if k not in seen:
            seen.add(k)
            out.append(c)
    return out[:20]


def task(args: tuple) -> dict:
    fname, pkg, mined = args
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    from r2py import heldout as ho
    from r2py.runtime import propose

    man = ho.load_manifest(str(ROOT / "experiments/dev_run/manifest.json"))
    cfg = man["protocol"]["translate"]
    package = None if pkg in ("base", "stats", "utils", "") else pkg
    with ho.pinned_llm(cfg["model"], ho.llm_settings(man)):
        rec = propose.attempt(fname, package, cfg["model"], rounds=8, attempts=4, mined=mined,
                              source_limit=15000, budget_s=1800, locate=True)
    rec["tag"] = "rd examples"
    rec["n_rd_cases"] = len(mined)
    propose.save(rec, OUT)
    return rec


def summarise(rows: list[dict]) -> str:
    lines = [f"{len(rows)} functions attempted with Rd-harvested cases",
             f"{'function':<28}{'status':<10}{'core':>8}{'cases':>7}{'rounds':>8}"]
    for r in sorted(rows, key=lambda r: (r.get("status") != "passed", r["function"])):
        lines.append(f"{(r['function'] + '@' + (r.get('package') or 'base'))[:26]:<28}"
                     f"{r.get('status', '?'):<10}"
                     f"{str(r.get('core_passed', '-')) + '/' + str(r.get('core_total', '-')):>8}"
                     f"{r.get('n_rd_cases', '-'):>7}{r.get('rounds', '-'):>8}")
    passed = [r for r in rows if r.get("status") == "passed"]
    lines.append(f"\npassed {len(passed)}/{len(rows)}: {', '.join(r['function'] for r in passed)}")
    return "\n".join(lines)


def main() -> int:
    from r2py.keepawake import keep_awake
    keep_awake()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--min-cases", type=int, default=3, help="skip functions with fewer harvested cases")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--summary-only", action="store_true")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    if args.summary_only:
        rows = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(OUT.glob("*.json"))]
        print(summarise(rows))
        return 0

    harvested = [json.loads(l) for l in HARVEST.open(encoding="utf-8")]
    tasks = []
    for row in harvested:
        mined = as_mined(row)
        if len(mined) < args.min_cases:
            continue
        done = OUT / f"{row['package'] or 'base'}__{row['function']}.json"
        if done.exists():
            continue
        tasks.append((row["function"], row["package"], mined))
    print(f"{len(tasks)} functions to attempt: "
          + ", ".join(f"{f}@{p} ({len(m)} cases)" for f, p, m in tasks), flush=True)
    ctx = multiprocessing.get_context("spawn")
    rows = []
    with ctx.Pool(args.workers) as pool:
        for rec in pool.imap_unordered(task, tasks):
            rows.append(rec)
            print(f"   {rec['function']:<24}{rec.get('status', '?'):<10}"
                  f"core {rec.get('core_passed', '-')}/{rec.get('core_total', '-')}  "
                  f"rounds {rec.get('rounds', '-')}", flush=True)
    print("\n" + summarise(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())

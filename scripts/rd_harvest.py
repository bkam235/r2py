"""Yield probe: can a package's own Rd examples supply the test cases the runtime pilot lacks?

Half of the pilot's package-function attempts never got a verdict (`no_cases`: R accepted fewer than
three of the model's invented calls), and corpus mining cannot help because the functions that cost
us points appear in one or two scripts in the whole 3,988-script corpus. Every exported function,
though, ships an `\\examples` block. This runs that block with the function intercepted in its own
namespace and records each real call: the arguments as evaluated at the call site, and R's answer.

No model calls. The question is the yield: how many usable cases per function, against the three
`propose.attempt` needs before it will even try.

    python scripts/rd_harvest.py --top 15
    python scripts/rd_harvest.py --functions time_add@timechange createTimeSlices@caret
"""
from __future__ import annotations

import argparse
import json
import multiprocessing
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

OUT = ROOT / "work" / "rd_harvest"

from r2py.runtime.harvest import _R_HARVEST, harvest  # noqa: E402,F401 (moved into the package)


def targets(top: int) -> list[str]:
    """The candidate functions that cost the held-out set the most, biggest first."""
    from collections import Counter

    from coverage_probe import heldout_entities
    from runtime_ceiling import PROBE, _classify, probe

    fns = {}
    for line in (PROBE / "heldout_functions.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        if "error" in r:
            continue
        for e in r["entities"]:
            fns[(r["script"], e["id"])] = (e["fn"], e["package"])
    ents = heldout_entities("empty")
    specs = sorted({fns[k] for k in ents if k in fns and fns[k][0]})
    info = probe(specs)
    loss: Counter = Counter()
    for k, v in ents.items():
        pair = fns.get(k)
        if pair and pair[0] and _classify(info.get(pair), pair[1]) == "candidate" and pair[1]:
            loss[f"{pair[0]}@{pair[1]}"] += 1 - v["mean"]
    return [s for s, _ in loss.most_common(top)], loss


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--top", type=int, default=15, help="the N candidate functions with the most held-out loss")
    ap.add_argument("--functions", nargs="+", default=None, help="explicit name@package list instead")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    loss: dict = {}
    if args.functions:
        specs = args.functions
    else:
        specs, loss = targets(args.top)
    print(f"{len(specs)} functions: {', '.join(specs)}", flush=True)
    ctx = multiprocessing.get_context("spawn")
    rows = []
    with ctx.Pool(args.workers) as pool:
        for row in pool.imap_unordered(harvest, specs):
            rows.append(row)
            print(f"   {row['function'] + '@' + row['package']:<34}{str(row.get('status'))[:22]:<24}"
                  f"cases {row.get('n_cases', 0):>3} ({row.get('n_distinct', 0)} distinct)  "
                  f"{row['seconds']}s", flush=True)
    (OUT / "rows.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    usable = [r for r in rows if (r.get("n_distinct") or 0) >= 3]
    print(f"\n{len(usable)}/{len(rows)} functions reach the 3 distinct cases the pilot needs")
    if loss:
        got = sum(loss[f"{r['function']}@{r['package']}"] for r in usable)
        want = sum(loss[s] for s in specs)
        print(f"held-out loss on those functions: {got:.1f} of {want:.1f} points covered "
              f"({got / want:.0%} of the targeted loss)")
    print(f"status counts: {json.dumps({s: sum(1 for r in rows if str(r.get('status')).startswith(s)) for s in sorted({str(r.get('status'))[:14] for r in rows})})}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

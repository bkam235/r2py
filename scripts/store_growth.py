"""C2: grow the runtime store over the training scripts with the on-demand step alone, and measure its hit rate.

The inter-script curve asks whether a store grown on earlier scripts helps later ones. The recurrence
curve (`recurrence_curves.py`) predicts the size from *hypothetical* functions - about 5.6% of held-out
loss reachable after 64 scripts, discounted by measured pass rates - far below what a cheap score
experiment can resolve. So this measures the mechanism with *real* verified functions instead:

1. the first N training scripts (manifest order) are taken with their saved translations and the
   per-entity scores already re-verified (`work/reverify/rows_v3.jsonl`) - no new translations;
2. the on-demand step runs on each (same settings as replay's `rewrite_w3_ondemand`), into one store
   directory that persists across scripts;
3. every admitted function is attributed to the script whose run added it, so the store after the
   first k scripts can be rebuilt for any k;
4. the hit rate of each snapshot is the share of held-out loss on entities whose function the store
   holds - structural, no model calls - next to the recurrence curve's prediction.

Workers run scripts in parallel, each reading the store when it starts, so a script does not see what
up to `workers - 1` scripts in flight add (the same staleness as parallel training); two workers can
attempt the same function, and the second finds it already there or attempts it again.

A run in which a provider call failed for good is discarded, not recorded; after three the driver stops
and the same command resumes.

    python scripts/store_growth.py run --n 64 --workers 4
    python scripts/store_growth.py report
"""
from __future__ import annotations

import argparse
import json
import multiprocessing
import pickle
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

MANIFEST = ROOT / "experiments" / "heldout" / "manifest.json"
ROWS = ROOT / "work" / "reverify" / "rows_v3.jsonl"
MAPS = ROOT / "work" / "reverify" / "script_maps"
STORE = ROOT / "work" / "runtime" / "store_growth"
OUT = ROOT / "work" / "store_growth"
ONDEMAND = dict(max_functions=2, budget_s=900, rounds=2, attempts=4)     # = replay's rewrite_w3_ondemand
SNAPSHOTS = (8, 16, 32, 64)


def report_from_row(row: dict) -> SimpleNamespace:
    """The per-entity scores the re-verification recorded, in the shape `ondemand` reads."""
    by = {}
    for e in row["entities"]:
        dims = e.get("active_dims") or []
        by[e["id"]] = SimpleNamespace(executed_ok=e.get("executed_ok", True), active_dims=dims,
                                      **{d: v for d, v in (e.get("dim_scores") or {}).items()})
    return SimpleNamespace(by_entity=by, aggregate=row.get("aggregate", 0.0))


def task(args: tuple) -> dict:
    index, script, row = args
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    from r2py import heldout as ho
    from r2py.runtime.ondemand import verify_needed
    from r2py.runtime.store import RuntimeStore
    from r2py.stage2 import llm

    man = ho.load_manifest(str(ROOT / "experiments/dev_run/manifest.json"))
    cfg = man["protocol"]["translate"]
    sm = pickle.loads((MAPS / f"{Path(script).stem}.pkl").read_bytes())
    store = RuntimeStore(STORE)
    before = set(store.entries)
    llm.drain_provider_failures()
    with ho.pinned_llm(cfg["model"], ho.llm_settings(man)):
        recs = verify_needed(sm, report_from_row(row), store, model=cfg["model"], log=lambda *_: None, **ONDEMAND)
    failed = llm.drain_provider_failures()
    out = {"index": index, "script": script, "records": recs, "store_before": len(before)}
    if failed:
        out["provider_unavailable"] = failed
        return out
    out["added"] = sorted(set(RuntimeStore(STORE).entries) - before)
    out["admitted"] = sorted(r["function"] for r in recs if r.get("admitted"))
    return out


def run(n: int, workers: int) -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = {r["script"]: r for r in map(json.loads, ROWS.open(encoding="utf-8")) if "error" not in r}
    order = [e["script"] for e in manifest["train"]
             if e["script"] in rows and (MAPS / f"{Path(e['script']).stem}.pkl").exists()][:n]
    OUT.mkdir(parents=True, exist_ok=True)
    STORE.mkdir(parents=True, exist_ok=True)
    path = OUT / "results.jsonl"
    done = {json.loads(l)["script"] for l in path.open(encoding="utf-8")} if path.exists() else set()
    tasks = [(i, s, rows[s]) for i, s in enumerate(order) if s not in done]
    print(f"{len(order)} scripts in order, {len(done)} done, {len(tasks)} to go, {workers} workers", flush=True)
    outages = 0
    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(workers) as pool, path.open("a", encoding="utf-8") as fh:
        for res in pool.imap(task, tasks):              # in order, so the log reads as the store grows
            if res.get("provider_unavailable"):
                outages += 1
                print(f"   #{res['index']:<3} provider unavailable {res['provider_unavailable']} - discarded", flush=True)
                if outages >= 3:
                    pool.terminate()
                    print("stopping after 3 provider outages; the same command resumes", flush=True)
                    break
                continue
            fh.write(json.dumps(res, default=str) + "\n")
            fh.flush()
            tried = [r.get("function") for r in res["records"] if r.get("function")]
            print(f"   #{res['index']:<3} {Path(res['script']).stem[:40]:<42} tried {tried}  "
                  f"admitted {res['admitted']}", flush=True)


def report() -> str:
    from coverage_probe import heldout_entities
    from r2py.runtime.difftest import py_name

    res = sorted((json.loads(l) for l in (OUT / "results.jsonl").open(encoding="utf-8")), key=lambda r: r["index"])
    pred = json.loads((ROOT / "work/coverage_probe/recurrence.json").read_text(encoding="utf-8"))
    pred = pred.get("function, held-out, discounted", {})
    fns = {}
    for line in (ROOT / "work/coverage_probe/heldout_functions.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        if "error" not in r:
            for e in r["entities"]:
                fns[(r["script"], e["id"])] = e["fn"]
    held = [(fns.get(k, ""), 1 - v["mean"]) for k, v in heldout_entities("empty").items()]
    total = sum(l for _, l in held)

    attempts = [rec for r in res for rec in r["records"] if rec.get("function")]
    status = {}
    for rec in attempts:
        k = rec.get("admitted") or rec.get("status") or "?"
        status[k] = status.get(k, 0) + 1
    lines = [f"{len(res)} scripts processed; {len(attempts)} function attempts: {status}", "",
             f"{'after N scripts':<17}{'functions':>10}{'held-out loss covered':>24}{'recurrence prediction':>24}"]
    for n in [k for k in SNAPSHOTS if k <= len(res)] + ([len(res)] if len(res) not in SNAPSHOTS else []):
        names = {f for r in res if r["index"] < n for f in r.get("admitted", [])}
        pys = {"r_" + py_name(f) for f in names}
        got = sum(l for fn, l in held if fn and "r_" + py_name(fn) in pys)
        p = pred.get(str(n))
        lines.append(f"{n:<17}{len(names):>10}{got / total:>23.1%}"
                     f"{(f'{p[0]:.1%}' if p else '-'):>24}")
    return "\n".join(lines)


def main() -> int:
    from r2py.keepawake import keep_awake
    keep_awake()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("run")
    p.add_argument("--n", type=int, default=64)
    p.add_argument("--workers", type=int, default=4)
    sub.add_parser("report")
    args = ap.parse_args()
    if args.cmd == "run":
        run(args.n, args.workers)
    text = report()
    print("\n" + text)
    (OUT / "report.txt").write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

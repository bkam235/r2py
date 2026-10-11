"""Re-score the final translation of every baseline replay run per entity and dimension (C1 step 1b).

The trajectories keep each accepted candidate's source and per-entity aggregate, not the dimensions,
so they cannot say what the partly-right entities get wrong (value, type, shape, printing, side
effects). This verifies each run's best accepted source again, with the replay's harness settings,
and keeps every entity's dimension scores and the verifier's feedback. No model calls (counted).

    python scripts/rescore_finals.py run --workers 4
    python scripts/rescore_finals.py summary
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import multiprocessing
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

MANIFEST = ROOT / "experiments/dev_run/manifest.json"
CACHE = ROOT / "work/replay/script_maps"
SOURCES = ["work/replay_ondemand/trajectories/*.rewrite_w3.[0-9].jsonl",
           "work/replay_oracle/trajectories/*.rewrite_w3.[0-9].jsonl"]
OUT = ROOT / "work/rescore_finals"


def _seeds() -> dict[str, str]:
    """source_hash -> source of every logged seed: a run that never improved ends on its start state,
    which its trajectory does not hold (replay.best_states took it from these seeds)."""
    out = {}
    for f in glob.glob(str(ROOT / "work/smoke/*/py/trajectories/*.jsonl")):
        for l in open(f, encoding="utf-8"):
            e = json.loads(l)
            if e["kind"] == "seed" and e.get("source"):
                out[e["source_hash"]] = e["source"]
    return out


def finals() -> list[dict]:
    seeds = _seeds()
    starts = {}
    for pat in SOURCES:
        for l in open(ROOT / Path(pat).parent.parent / "results.jsonl", encoding="utf-8"):
            r = json.loads(l)
            starts[(r["script"], r["policy"], r["sample"])] = r
    out = []
    for pat in SOURCES:
        for f in sorted(glob.glob(str(ROOT / pat))):
            ev = [json.loads(l) for l in open(f, encoding="utf-8")]
            if ev[-1]["kind"] != "run_end":
                continue
            acc = [e for e in ev if e["kind"] == "accepted" and e.get("source")]
            if acc:
                best = max(acc, key=lambda e: e.get("aggregate") or 0)
            else:                            # never improved: the final state is the start state
                r = starts[(ev[0]["script"], ev[0]["policy"], ev[0]["sample"])]
                best = {"source": seeds[r["start_hash"]], "aggregate": r["start_score"]}
            out.append({"run": f"{Path(f).parent.parent.name}/{Path(f).name}", "script": ev[0]["script"],
                        "source": best["source"], "logged_aggregate": best.get("aggregate"),
                        "logged_per_entity": best.get("per_entity") or {}})
    return out


def one(task: dict) -> dict:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    from r2py import heldout as ho
    from r2py.harness.tools import HarnessTools
    from r2py.library import PatternLibrary
    from r2py.stage2 import llm
    from scripts.replay import _script_map

    calls = [0]
    real = llm.call

    def counted(*a, **k):
        calls[0] += 1
        return real(*a, **k)
    llm.call = counted
    row = {k: task[k] for k in ("run", "script", "logged_aggregate")}
    started = time.monotonic()
    try:
        manifest = ho.load_manifest(str(MANIFEST))
        cfg = manifest["protocol"]["translate"]
        sm = _script_map(task["script"], manifest, CACHE)
        with ho.pinned_llm(cfg["model"], ho.llm_settings(manifest)):
            tools = HarnessTools(sm, PatternLibrary(OUT / "empty_lib"), model=cfg["model"],
                                 data_compare=cfg["data_compare"], timeout_s=cfg["timeout_s"],
                                 sidecar_filename=f"{Path(task['script']).stem}.r2py_data.json")
            tools.note_reference(task["source"])
            report = tools.verify(task["source"])
        ents = []
        for rec in ho._entity_records(sm, report):
            fb = [f"{f.effect_class.value}: {f.message}"[:220] for f in report.feedback if f.entity_id == rec["id"]][:4]
            ents.append({k: rec[k] for k in ("id", "name", "active_dims", "dim_scores", "executed_ok", "uncomparable")}
                        | {"score": (report.by_entity[rec["id"]].aggregate
                                     if hasattr(report.by_entity[rec["id"]], "aggregate") else None),
                           "logged": task["logged_per_entity"].get(rec["id"]), "feedback": fb})
        row.update(aggregate=round(report.aggregate, 4), py_exit=report.py_exit_code, entities=ents)
    except Exception as exc:
        row["error"] = f"{type(exc).__name__}: {exc}"[:300]
    row["llm_calls"] = calls[0]
    row["seconds"] = round(time.monotonic() - started, 1)
    llm.call = real
    return row


def run(workers: int) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "rows.jsonl"
    done = {json.loads(l)["run"] for l in path.open(encoding="utf-8")} if path.exists() else set()
    todo = [t for t in finals() if t["run"] not in done]
    print(f"{len(done)} done, {len(todo)} to go, {workers} workers", flush=True)
    with multiprocessing.get_context("spawn").Pool(workers) as pool, path.open("a", encoding="utf-8") as fh:
        for i, row in enumerate(pool.imap_unordered(one, todo), start=1):
            fh.write(json.dumps(row, default=str) + "\n")
            fh.flush()
            mark = row.get("error") or f"{row['aggregate']:.3f} (logged {row['logged_aggregate']})"
            print(f"{i}/{len(todo)} {row['run'][:70]:<72} {mark} {row['seconds']}s llm={row['llm_calls']}", flush=True)


def summary() -> str:
    rows = [json.loads(l) for l in (OUT / "rows.jsonl").open(encoding="utf-8")]
    ok = [r for r in rows if "error" not in r]
    lines = [f"{len(rows)} runs re-scored, {len(rows) - len(ok)} errors, "
             f"{sum(r['llm_calls'] for r in rows)} model calls"]
    drift = [abs(r["aggregate"] - (r["logged_aggregate"] or 0)) for r in ok]
    lines.append(f"aggregate vs logged: mean |diff| {sum(drift) / max(1, len(drift)):.3f}, "
                 f"{sum(d > 0.05 for d in drift)} runs differ by > 0.05")
    loss = collections.Counter()
    n = collections.Counter()
    worst = collections.Counter()
    fb = collections.Counter()
    for r in ok:
        for e in r["entities"]:
            if e["uncomparable"] or not e["active_dims"]:
                continue
            dims = e["dim_scores"]
            s = sum(dims.values()) / len(dims)
            if s >= 0.9:
                continue
            band = "not executed" if not e["executed_ok"] else ("partial" if s >= 0.1 else "zero")
            n[band] += 1
            for d, v in dims.items():
                loss[(band, d)] += 1 - v
            worst[(band, min(dims, key=dims.get))] += 1
            for f in e["feedback"]:
                fb[(band, f.split(":")[0])] += 1
    total = sum(loss.values()) or 1
    lines.append(f"entities below 0.9: {dict(n)}")
    lines.append("loss by (band, dimension), share of all dimension loss:")
    lines += [f"  {b:<13} {d:<20} {v / total:6.1%}" for (b, d), v in loss.most_common()]
    lines.append("worst dimension per entity:")
    lines += [f"  {b:<13} {d:<20} {c}" for (b, d), c in worst.most_common()]
    lines.append("feedback items by effect class:")
    lines += [f"  {b:<13} {d:<20} {c}" for (b, d), c in fb.most_common()]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("run")
    p.add_argument("--workers", type=int, default=4)
    sub.add_parser("summary")
    args = ap.parse_args()
    if args.cmd == "run":
        run(args.workers)
    text = summary()
    print("\n" + text)
    (OUT / "summary.txt").write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

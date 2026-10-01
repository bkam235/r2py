"""Why do seed translations fail?  Re-run the logged seed sources and classify what happens.

The trajectory logs hold every seed's source and score, not why it crashed.  This re-verifies each
unique seed source (no model calls: the entity mapping is read off the sentinels it carries) and
records the exception that ended it, whether the agent loop's cheap gates would have caught it,
and the seed's kind, so the failure classes can be ranked.

    python scripts/diagnose_seeds.py --arms work/smoke/20261001_112951 work/smoke/20261001_140509 ...
"""
from __future__ import annotations

import argparse
import collections
import json
import multiprocessing
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

EXC_RE = re.compile(r"^([A-Za-z_][\w.]*(?:Error|Exception|Exit|Interrupt|Warning)|TimeoutExpired)\b:?\s*(.*)$")


def classify(stderr: str, exit_code: int) -> tuple[str, str]:
    """(class, detail) from a traceback: the last exception line decides."""
    if exit_code == 0:
        return "ran", ""
    last = ""
    for line in reversed((stderr or "").strip().splitlines()):
        if EXC_RE.match(line.strip()):
            last = line.strip()
            break
    if not last:
        return ("timeout" if "exceeded" in (stderr or "") else "no_traceback"), (stderr or "").strip()[-120:]
    m = EXC_RE.match(last)
    exc, msg = m.group(1), m.group(2)
    exc = exc.split(".")[-1]
    if exc in ("ModuleNotFoundError", "ImportError"):
        mod = re.search(r"No module named '([^']+)'", msg) or re.search(r"cannot import name '([^']+)'", msg)
        return "import", (mod.group(1) if mod else msg[:60])
    if exc in ("SyntaxError", "IndentationError", "TabError"):
        return "syntax", msg[:60]
    if exc == "AttributeError":
        obj = re.search(r"'([^']+)' object has no attribute '([^']+)'", msg) or re.search(
            r"module '([^']+)' has no attribute '([^']+)'", msg)
        return "attribute", f"{obj.group(1)}.{obj.group(2)}" if obj else msg[:60]
    if exc == "TypeError":
        kw = re.search(r"unexpected keyword argument '([^']+)'", msg)
        return "type_error", f"unexpected kwarg {kw.group(1)}" if kw else msg[:60]
    if exc == "NameError":
        return "name", msg[:60]
    if exc in ("KeyError", "IndexError", "ValueError", "AssertionError", "NotImplementedError",
               "RecursionError", "ZeroDivisionError", "FileNotFoundError", "OSError"):
        return exc, msg[:60]
    return "other", f"{exc}: {msg[:50]}"


def work(task: tuple) -> list[dict]:
    """One script: analyze once, verify each unique seed source."""
    name, seeds, manifest_path = task
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    from r2py import heldout as ho
    from r2py.harness.agent import _check_syntax
    from r2py.stage0.env.module_check import unavailable_imports
    from r2py.stage0.sandbox.py_sandbox import _SKIP_PACKAGES
    from r2py.stage1 import analyze
    from r2py.stage2.argorder import repair_argument_order
    from r2py.stage2.sentinel_mapper import flatten_entity_line_map, ranges_from_sentinels, strip_sentinels
    from r2py.stage4 import verifier

    manifest = ho.load_manifest(manifest_path)
    cfg = manifest["protocol"]["translate"]
    pool = ho._pool_path(manifest)
    if not pool.is_absolute():
        pool = ROOT / pool
    sm = analyze(next(pool.rglob(name)))
    out = []
    for seed in seeds:
        src = seed["source"]
        row = {"script": name, "label": seed["label"], "logged_agg": seed["aggregate"], "arm": seed["arm"]}
        clean = strip_sentinels(src)
        try:
            rep, bundle = verifier.verify(
                sm, clean, data_compare=cfg["data_compare"],
                entity_line_map=flatten_entity_line_map(ranges_from_sentinels(src)),
                sidecar_filename=f"{Path(name).stem}.r2py_data.json", timeout_s=cfg["timeout_s"],
                return_bundle=True)
            row.update(aggregate=round(rep.aggregate, 4), exit_code=rep.py_exit_code)
            row["class"], row["detail"] = classify(bundle.stderr, rep.py_exit_code)
        except Exception as exc:  # a harness failure is not a translation failure; record it
            row.update(aggregate=None, exit_code=None)
            row["class"], row["detail"] = "harness_error", f"{type(exc).__name__}: {exc}"[:100]
        # What the agent loop's cheap gates would say about this source.
        row["syntax_gate"] = bool(_check_syntax(src))
        row["import_gate"] = unavailable_imports(clean, _SKIP_PACKAGES)
        row["argorder_would_change"] = repair_argument_order(clean)[1] > 0
        out.append(row)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", nargs="+", required=True)
    ap.add_argument("--manifest", default=str(ROOT / "experiments/dev_run/manifest.json"))
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--out", default=str(ROOT / "work/seed_diagnosis.json"))
    args = ap.parse_args()

    from r2py.harness import trajectory

    by_script: dict[str, dict[str, dict]] = collections.defaultdict(dict)   # script -> source hash -> seed
    for arm in args.arms:
        for f in sorted((Path(arm) / "py" / "trajectories").glob("*.jsonl")):
            recs = trajectory.read(f)
            name = recs[0]["script"]
            for r in recs:
                if r["kind"] == "seed" and r.get("source"):
                    by_script[name].setdefault(r["source_hash"], {
                        "label": r["label"], "aggregate": r["aggregate"], "source": r["source"],
                        "arm": Path(arm).name[-6:]})
    tasks = [(n, list(v.values()), args.manifest) for n, v in sorted(by_script.items())]
    print(f"{sum(len(t[1]) for t in tasks)} unique seeds over {len(tasks)} scripts", flush=True)

    ctx = multiprocessing.get_context("spawn")
    rows: list[dict] = []
    with ctx.Pool(args.workers) as pool:
        for i, res in enumerate(pool.imap_unordered(work, tasks), 1):
            rows += res
            print(f"[{i}/{len(tasks)}] {res[0]['script'][:50]}: {sum(r['class'] == 'ran' for r in res)}/{len(res)} ran",
                  flush=True)
    Path(args.out).write_text(json.dumps(rows, indent=1), encoding="utf-8")

    n = len(rows)
    print(f"\n{n} seeds re-verified; {sum(r['class'] == 'ran' for r in rows)} ran")
    c = collections.Counter(r["class"] for r in rows)
    print("\nOutcome classes:")
    for k, v in c.most_common():
        print(f"  {k:14s} {v:4d}  {v / n:.0%}")
    fails = [r for r in rows if r["class"] != "ran"]
    print("\nMost common causes among failing seeds:")
    for (k, d), v in collections.Counter((r["class"], r["detail"]) for r in fails).most_common(18):
        print(f"  {v:3d}  {k}: {d}")
    print("\nWould the agent loop's cheap gates have flagged the failing seeds?")
    print(f"  syntax gate: {sum(r['syntax_gate'] for r in fails)}   import gate: {sum(bool(r['import_gate']) for r in fails)}   "
          f"argument order would change: {sum(r['argorder_would_change'] for r in fails)}   of {len(fails)}")
    for kind in ("Bare", "Structured"):
        ks = [r for r in rows if r["label"].startswith(kind)]
        print(f"  {kind:10s} ran {sum(r['class'] == 'ran' for r in ks)}/{len(ks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

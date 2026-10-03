"""Which R classes do the corpus' data entities have?  (Stage 4 Phase 1: the adapter worklist, R side only.)

Runs ``analyze`` (R only, no model calls) on the manifest's scripts and tallies the R class of every captured
variable, so adapters are written for families the corpus actually contains.  The Python side's exclusions
(Phase 0 ``excluded`` rows) say which of them could not be serialised there.

    python scripts/census_data_classes.py --workers 6 [--split heldout|train|all]
"""
from __future__ import annotations

import argparse
import collections
import json
import multiprocessing
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

BASIC = {"numeric", "character", "integer", "logical", "double", "complex", "list", "NULL", "function",
         "data.frame", "tbl_df", "tbl", "factor", "Date", "POSIXct", "POSIXt", "matrix", "array", "environment"}


def work(task: tuple) -> dict:
    name, manifest_path = task
    from r2py import heldout as ho
    from r2py.stage1 import analyze

    manifest = ho.load_manifest(manifest_path)
    pool = ho._pool_path(manifest)
    if not pool.is_absolute():
        pool = ROOT / pool
    started = time.monotonic()
    try:
        sm = analyze(next(pool.rglob(name)))
        vars_ = [(var, info.get("class", "")) for ent in (getattr(sm, "entity_types", None) or {}).values()
                 for var, info in ent.items() if isinstance(info, dict)]
        # What the comparators will see of each captured variable: its numeric fields and text forms (values
        # truncated), kept for scripts/fingerprint_null_report.py.
        from r2py.stage4.comparators import fingerprint as fp
        from r2py.stage4.verifier import get_r_bundle
        captured = {}
        for var, val in (getattr(get_r_bundle(sm), "data", {}) or {}).items():
            fields = [(path, vec[:2000]) for path, vec in fp.numeric_fields(val)][:200]
            captured[var] = {"fp": fp.is_fp(val), "fields": fields, "texts": [t[:300] for t in fp.texts(val)][:2]}
        return {"script": name, "vars": vars_, "captured": captured, "seconds": round(time.monotonic() - started, 1)}
    except Exception as exc:
        return {"script": name, "error": f"{type(exc).__name__}: {exc}"[:200]}


def main() -> int:
    from r2py.keepawake import keep_awake
    keep_awake()
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--split", choices=("heldout", "train", "all"), default="all")
    ap.add_argument("--manifest", default=str(ROOT / "experiments/heldout/manifest.json"))
    ap.add_argument("--out", default=str(ROOT / "work/census/fields.jsonl"))
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    from r2py import heldout as ho
    manifest = ho.load_manifest(args.manifest)
    names = []
    if args.split in ("heldout", "all"):
        names += [e["script"] for e in manifest["heldout"]]
    if args.split in ("train", "all"):
        names += [e["script"] if isinstance(e, dict) else e for e in manifest["train"]]
    names = names[: args.limit] if args.limit else names
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)["script"] for l in out.read_text(encoding="utf-8").splitlines() if l.strip()} if out.exists() else set()
    tasks = [(n, args.manifest) for n in names if n not in done]
    print(f"{len(tasks)} scripts ({len(done)} done), {args.workers} workers", flush=True)
    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(args.workers) as pool, out.open("a", encoding="utf-8") as f:
        for i, row in enumerate(pool.imap_unordered(work, tasks), 1):
            f.write(json.dumps(row) + "\n")
            f.flush()
            print(f"[{i}/{len(tasks)}] {row['script'][:60]} " + (row["error"] if "error" in row else f"{len(row['vars'])} vars"), flush=True)
    rows = [json.loads(l) for l in out.read_text(encoding="utf-8").splitlines() if l.strip()]
    ok = [r for r in rows if "vars" in r]
    tally = collections.Counter()
    scripts_with = collections.defaultdict(set)
    for r in ok:
        for _v, cls in r["vars"]:
            key = cls if isinstance(cls, str) else json.dumps(cls)
            tally[key] += 1
            scripts_with[key].add(r["script"])
    print(f"\n{len(ok)} scripts analysed, {len(rows) - len(ok)} failed; R classes of captured variables (not basic):")
    for cls, n in [(c, n) for c, n in tally.most_common() if c.split(",")[0].strip("[]\" ") not in BASIC][:40]:
        print(f"  {n:5d} vars in {len(scripts_with[cls]):3d} scripts  {cls[:90]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

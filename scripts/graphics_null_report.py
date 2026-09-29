"""Null-rate report: how much of the graphics dimension the fingerprints can actually judge.

For each R script it runs the real Stage 1 pipeline and reports pages captured, pages whose
fingerprint is null (extraction failed or unsupported), and which plotting systems appear.
A page that is null on either side is skipped by the comparator, so this rate bounds how much
of the graphics score rests on content rather than on page counts.

    python scripts/graphics_null_report.py                         # the 60 held-out scripts
    python scripts/graphics_null_report.py --pool 100              # plus a sample of the pool
    python scripts/graphics_null_report.py --python-dir work/heldout/outputs/full/rep0
        # also fingerprints the saved Python translations of scripts that plot

Slow (each script is run in R); results stream to the terminal and to --out (JSON).
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

MANIFEST = ROOT / "experiments" / "heldout" / "manifest.json"


def _system(fp: dict | None) -> str:
    return "null" if fp is None else fp.get("src", "?")


def _nullness(fp: dict | None) -> str:
    """A non-null fingerprint can still be empty of content (nothing extracted)."""
    if fp is None:
        return "null"
    has_content = any(fp.get(k) for k in ("px", "bars", "n_polys", "n_segs", "n_img", "texts"))
    return "ok" if has_content else "empty"


def r_side(script: Path) -> dict:
    from r2py.stage1 import analyze
    from r2py.stage4.verifier import _get_r_bundle

    sm = analyze(script)
    b = _get_r_bundle(sm)
    entity_pages = sum(len(v.graphics_meta) for v in (sm.entity_bundles or {}).values())
    return {"pages": len(b.graphics), "meta": b.graphics_meta,
            "entity_pages": entity_pages,
            "entities_with_plots": sum(1 for v in (sm.entity_bundles or {}).values() if v.graphics_meta),
            "source_uses_plots": bool(b.graphics or b.graphics_meta)}, sm


def python_side(sm, py_path: Path, script_stem: str) -> dict | None:
    from r2py.stage2.sentinel_mapper import strip_sentinels
    from r2py.stage4 import verifier

    if not py_path.exists():
        return None
    src = strip_sentinels(py_path.read_text(encoding="utf-8"))
    _, pb = verifier.verify(sm, src, sidecar_filename=f"{script_stem}.r2py_data.json",
                            timeout_s=120, return_bundle=True)
    return {"pages": len(pb.graphics), "meta": pb.graphics_meta}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", type=int, default=0, help="also sample N non-held-out pool scripts")
    ap.add_argument("--python-dir", type=Path, help="dir of saved Python translations")
    ap.add_argument("--out", type=Path, default=ROOT / "work" / "graphics_null_report.json")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    pool = ROOT / manifest["pool_dir"]
    scripts = [e["script"] for e in manifest["heldout"]]
    if args.pool:
        rest = sorted({p.name for p in pool.rglob("*.R")} - set(scripts))
        scripts += random.Random(args.seed).sample(rest, min(args.pool, len(rest)))

    results, errors = [], []
    for i, name in enumerate(scripts, 1):
        path = next(pool.rglob(name), None)
        if path is None:
            continue
        try:
            r, sm = r_side(path)
            py = python_side(sm, args.python_dir / (path.stem + ".py"), path.stem) \
                if args.python_dir and r["pages"] else None
        except Exception as exc:  # a script that cannot run says nothing about fingerprints
            errors.append((name, f"{type(exc).__name__}: {exc}"[:200]))
            print(f"[{i}/{len(scripts)}] {name}: ERROR {errors[-1][1]}", flush=True)
            continue
        row = {"script": name, "r": {k: r[k] for k in ("pages", "entity_pages", "entities_with_plots")},
               "r_kinds": [_nullness(fp) + ":" + _system(fp) for fp in r["meta"]]}
        if py is not None:
            row["py"] = {"pages": py["pages"]}
            row["py_kinds"] = [_nullness(fp) + ":" + _system(fp) for fp in py["meta"]]
        results.append(row)
        if r["pages"]:
            print(f"[{i}/{len(scripts)}] {name}: R pages={r['pages']} {Counter(row['r_kinds'])}", flush=True)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"results": results, "errors": errors}, indent=1), encoding="utf-8")

    plotters = [r for r in results if r["r"]["pages"]]
    kinds = Counter(k for r in plotters for k in r["r_kinds"])
    n_pages = sum(kinds.values())
    print(f"\nscripts run: {len(results)} ({len(errors)} could not run)")
    print(f"scripts that plot: {len(plotters)}  ({len(plotters) / max(len(results), 1):.0%})")
    print(f"R pages: {n_pages}")
    for k, n in kinds.most_common():
        print(f"   {k:16s} {n:4d}  {n / max(n_pages, 1):.0%}")
    usable = sum(n for k, n in kinds.items() if k.startswith("ok:"))
    print(f"R pages with a usable fingerprint: {usable}/{n_pages} ({usable / max(n_pages, 1):.0%})")
    print(f"entity-level: {sum(r['r']['entities_with_plots'] for r in plotters)} entities carry plots")
    pyrows = [r for r in plotters if "py_kinds" in r]
    if pyrows:
        pk = Counter(k for r in pyrows for k in r["py_kinds"])
        print(f"\nPython translations of plotting scripts: {len(pyrows)}; pages by kind: {dict(pk)}")
        both = sum(1 for r in pyrows if r["r"]["pages"] == r["py"]["pages"])
        print(f"   page count matches R in {both}/{len(pyrows)}")
    for name, err in errors:
        print(f"   ERROR {name}: {err}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

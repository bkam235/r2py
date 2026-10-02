"""Evaluate the seed stage alone: P(run), P(>=0.5), mean score, and best-of-k per script.

Every seed is an independent sample, so ~100 seeds per variant resolve differences that a 24-script
whole-run arm cannot (the seed stage also differs between whole-run arms in about half the scripts).
No agent runs: each seed is generated exactly as the loop does it (``r2py.seed.translate``) and verified.

    python scripts/seed_eval.py --name gate_on  --gate on  --schedule bare:2 structured:2
    python scripts/seed_eval.py --name gate_off --gate off --schedule bare:2 structured:2
    python scripts/seed_eval.py --summary work/seed_eval/gate_off.jsonl work/seed_eval/gate_on.jsonl

Rows are appended to work/seed_eval/<name>.jsonl as seeds finish; a rerun skips finished ones.
"""
from __future__ import annotations

import argparse
import collections
import json
import multiprocessing
import shutil
import statistics as st
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))


def seed_task(task: dict) -> dict:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    import diagnose_seeds
    import replay
    from r2py import heldout as ho
    from r2py import lessons as lessons_mod
    from r2py import seed as seed_mod
    from r2py.library import PatternLibrary
    from r2py.stage2.sentinel_mapper import strip_sentinels
    from r2py.stage4 import verifier

    manifest = ho.load_manifest(task["manifest"])
    cfg = manifest["protocol"]["translate"]
    row = {k: task[k] for k in ("script", "kind", "idx")}
    started = time.monotonic()
    seed_mod.seed_gate_stats.clear()
    try:
        with ho.pinned_llm(cfg["model"], ho.llm_settings(manifest)):
            sm = replay._script_map(task["script"], manifest, Path(task["cache"]))
            stem = Path(task["script"]).stem
            with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
                shutil.copytree(Path(task["library"]), Path(tmp) / "lib")
                source, elmap = seed_mod.translate(
                    sm, PatternLibrary(Path(tmp) / "lib"), model=cfg["model"],
                    sidecar_filename=f"{stem}.r2py_data.json", script_relpath=f"work/seed_eval/{stem}.py",
                    bare=task["kind"] == "bare", gate=task["gate"],
                    lessons=lessons_mod.load(task["lessons"]) if task.get("lessons") else None)
            rep, bundle = verifier.verify(
                sm, source, data_compare=cfg["data_compare"], entity_line_map=elmap,
                sidecar_filename=f"{stem}.r2py_data.json", timeout_s=cfg["timeout_s"], return_bundle=True)
            row.update(aggregate=round(rep.aggregate, 4), exit_code=rep.py_exit_code,
                       source_hash=__import__("hashlib").sha1(strip_sentinels(source).encode()).hexdigest()[:12])
            row["class"], row["detail"] = diagnose_seeds.classify(bundle.stderr, rep.py_exit_code)
            row["gate"] = dict(seed_mod.seed_gate_stats)
    except Exception as exc:
        row["error"] = f"{type(exc).__name__}: {exc}"[:300]
    row["seconds"] = round(time.monotonic() - started, 1)
    return row


def summarise(paths: list[str]) -> str:
    lines = []
    for p in paths:
        rows = [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]
        ok = [r for r in rows if "aggregate" in r]
        if not ok:
            lines.append(f"{p}: no finished seeds")
            continue
        n = len(ok)
        lines.append(f"\n== {Path(p).stem}: {n} seeds ({len(rows) - n} errors) over {len({r['script'] for r in ok})} scripts")
        lines.append(f"  P(runs) {sum(r['exit_code'] == 0 for r in ok) / n:.0%}   P(>=0.5) {sum(r['aggregate'] >= 0.5 for r in ok) / n:.0%}"
                     f"   P(>=0.9) {sum(r['aggregate'] >= 0.9 for r in ok) / n:.0%}   mean {st.mean(r['aggregate'] for r in ok):.3f}")
        for kind in ("bare", "structured"):
            ks = [r for r in ok if r["kind"] == kind]
            if ks:
                lines.append(f"  {kind:10s} n={len(ks):3d}  P(runs) {sum(r['exit_code'] == 0 for r in ks) / len(ks):.0%}  "
                             f"P(>=0.5) {sum(r['aggregate'] >= 0.5 for r in ks) / len(ks):.0%}  mean {st.mean(r['aggregate'] for r in ks):.3f}")
        by = collections.defaultdict(list)
        for r in ok:
            by[r["script"]].append(r["aggregate"])
        lines.append(f"  best seed per script, mean over scripts: {st.mean(max(v) for v in by.values()):.3f}   "
                     f"scripts with no seed >0: {sum(max(v) == 0 for v in by.values())}/{len(by)}")
        g = collections.Counter()
        for r in ok:
            g.update(r.get("gate", {}))
        if g:
            lines.append(f"  seed gate: {dict(g)}")
        causes = collections.Counter((r["class"], r["detail"]) for r in ok if r["class"] != "ran")
        lines.append("  top failure causes: " + "; ".join(f"{v}x {k}: {d}" for (k, d), v in causes.most_common(6)))
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name")
    ap.add_argument("--gate", choices=("on", "off"), default="on")
    ap.add_argument("--schedule", nargs="+", default=["bare:2", "structured:2"], help="kind:count ...")
    ap.add_argument("--only", nargs="+")
    ap.add_argument("--lessons", help="lesson store (JSON) offered in the seed gate's corrective turn")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--manifest", default=str(ROOT / "experiments/dev_run/manifest.json"))
    ap.add_argument("--library", default=str(ROOT / "work/dev_run/checkpoints/empty"))
    ap.add_argument("--summary", nargs="+")
    args = ap.parse_args()
    if args.summary:
        print(summarise(args.summary))
        return 0

    from r2py import heldout as ho
    manifest = ho.load_manifest(args.manifest)
    scripts = [e["script"] for e in manifest["heldout"]]
    if args.only:
        scripts = [s for s in scripts if any(o in s for o in args.only)]
    out = ROOT / "work" / "seed_eval" / f"{args.name}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        done = {(r["script"], r["kind"], r["idx"]) for r in (json.loads(l) for l in out.read_text(encoding="utf-8").splitlines() if l.strip())
                if "aggregate" in r}
    kinds = []
    for item in args.schedule:
        kind, count = item.split(":")
        kinds += [(kind, i) for i in range(int(count))]
    tasks = [dict(script=s, kind=k, idx=i, gate=args.gate == "on", lessons=args.lessons, manifest=args.manifest, library=args.library,
                  cache=str(ROOT / "work/replay/script_maps"))
             for (k, i) in kinds for s in scripts if (s, k, i) not in done]
    print(f"{len(tasks)} seeds to generate ({len(done)} done), {args.workers} workers", flush=True)
    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(args.workers) as pool, out.open("a", encoding="utf-8") as f:
        for i, row in enumerate(pool.imap_unordered(seed_task, tasks), 1):
            f.write(json.dumps(row) + "\n")
            f.flush()
            print(f"[{i}/{len(tasks)}] {row['script'][:36]:36s} {row['kind']:10s} #{row['idx']}: "
                  + (f"{row['aggregate']:.2f} {row['class']} {row['detail'][:40]}" if "aggregate" in row
                     else f"ERROR {row['error'][:80]}"), flush=True)
    print(summarise([str(out)]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

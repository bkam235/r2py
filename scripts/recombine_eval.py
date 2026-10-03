"""Does recombining seeds beat the best single seed?  (Stage 11b; no model calls.)

For each script the logged seed sources of the given arms are re-verified with the current harness.  A
*draw* is a random subset of ``--pool`` of them (the loop generates about four); ``recombine`` is run on it
and its result compared with the best seed of the same subset, paired by (script, draw).

    python scripts/recombine_eval.py --arms work/smoke/20261001_112951 ... --pool 4 --draws 3 --workers 6
    python scripts/recombine_eval.py --summary work/recombine/results.jsonl
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import multiprocessing
import random
import shutil
import statistics as st
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))


def load_seeds(arms: list[str]) -> dict[str, list[str]]:
    """script -> unique annotated seed sources across the arms' trajectory logs."""
    from r2py.harness import trajectory

    out: dict[str, dict[str, str]] = collections.defaultdict(dict)
    for arm in arms:
        for f in sorted((Path(arm) / "py" / "trajectories").glob("*.jsonl")):
            recs = trajectory.read(f)
            for r in recs:
                if r["kind"] == "seed" and r.get("source"):
                    out[recs[0]["script"]].setdefault(r["source_hash"], r["source"])
    return {k: list(v.values()) for k, v in out.items()}


def work(task: dict) -> list[dict]:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    import replay
    from r2py import heldout as ho
    from r2py.harness import objective as obj
    from r2py.harness import recombine as recombine_mod
    from r2py.harness.recombine import recombine
    from r2py.harness.tools import HarnessTools
    from r2py.library import PatternLibrary

    manifest = ho.load_manifest(task["manifest"])
    cfg = manifest["protocol"]["translate"]
    script, seeds = task["script"], task["seeds"]
    rows: list[dict] = []
    started = time.monotonic()
    try:
        with ho.pinned_llm(cfg["model"], ho.llm_settings(manifest)):
            sm = replay._script_map(script, manifest, Path(task["cache"]))
            with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
                shutil.copytree(Path(task["library"]), Path(tmp) / "lib")
                harness = HarnessTools(sm, PatternLibrary(Path(tmp) / "lib"), model=cfg["model"],
                                       data_compare=cfg["data_compare"], timeout_s=cfg["timeout_s"],
                                       sidecar_filename=f"{Path(script).stem}.r2py_data.json")
                reports = {}
                for s in seeds:
                    harness.note_reference(s)
                    reports[s] = harness.verify(s)
                rng = random.Random(int(hashlib.sha1(script.encode()).hexdigest(), 16) % 10 ** 6)
                for d in range(task["draws"]):
                    sub = rng.sample(seeds, min(task["pool"], len(seeds)))
                    if len(sub) < 2:
                        continue
                    pool = [(s, reports[s]) for s in sub]
                    best_src, best_rep = pool[0]
                    for s, r in pool[1:]:
                        if obj.better(r, best_rep):
                            best_src, best_rep = s, r
                    recombine_mod.stats.clear()
                    res = recombine(pool, harness)
                    final = res[1] if res else best_rep
                    rows.append(dict(script=script, draw=d, pool=len(sub), best_single=round(best_rep.aggregate, 4),
                                     best_single_runs=best_rep.py_exit_code == 0,
                                     recombined=round(final.aggregate, 4), final_runs=final.py_exit_code == 0,
                                     changed=res is not None, stats=dict(recombine_mod.stats)))
    except Exception as exc:
        rows.append(dict(script=script, error=f"{type(exc).__name__}: {exc}"[:300]))
    for r in rows:
        r["seconds"] = round(time.monotonic() - started, 1)
    return rows


def summarise(rows: list[dict]) -> str:
    ok = [r for r in rows if "recombined" in r]
    if not ok:
        return "no finished draws"
    a = [r["best_single"] for r in ok]
    b = [r["recombined"] for r in ok]
    d = [y - x for x, y in zip(a, b)]
    lines = [f"{len(ok)} draws over {len({r['script'] for r in ok})} scripts (pool {st.mean(r['pool'] for r in ok):.1f} seeds)",
             f"best single seed: mean {st.mean(a):.3f}   recombined: mean {st.mean(b):.3f}   diff {st.mean(d):+.3f}",
             f"recombination changed the result in {sum(r['changed'] for r in ok)}/{len(ok)} draws; "
             f"better/worse/tied {sum(x > .01 for x in d)}/{sum(x < -.01 for x in d)}/{sum(abs(x) <= .01 for x in d)}",
             f"runs to completion: best single {sum(r['best_single_runs'] for r in ok)}  recombined {sum(r['final_runs'] for r in ok)}  of {len(ok)}"]
    c = collections.Counter()
    for r in ok:
        c.update(r.get("stats", {}))
    if c:
        lines.append("what recombination did per entity tried: " + ", ".join(f"{k} {v}" for k, v in sorted(c.items())))
    by = collections.defaultdict(list)
    for r in ok:
        by[r["script"]].append(r["recombined"] - r["best_single"])
    sd = [st.mean(v) for v in by.values()]
    if len(sd) > 1:
        try:
            from scipy.stats import wilcoxon
            p = float(wilcoxon(sd).pvalue) if any(abs(x) > 1e-9 for x in sd) else 1.0
        except ImportError:
            p = float("nan")
        lines.append(f"per script (mean over draws): {st.mean(sd):+.3f}  SE {st.stdev(sd) / len(sd) ** .5:.3f}  Wilcoxon p={p:.3f}")
    gains = sorted(((st.mean(v), k) for k, v in by.items()), reverse=True)[:5]
    lines.append("largest gains: " + "; ".join(f"{k[:28]} {v:+.2f}" for v, k in gains))
    return "\n".join(lines)


def main() -> int:
    from r2py.keepawake import keep_awake
    keep_awake()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arms", nargs="+")
    ap.add_argument("--pool", type=int, default=4)
    ap.add_argument("--draws", type=int, default=3)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--only", nargs="+")
    ap.add_argument("--manifest", default=str(ROOT / "experiments/dev_run/manifest.json"))
    ap.add_argument("--library", default=str(ROOT / "work/dev_run/checkpoints/empty"))
    ap.add_argument("--out", default=str(ROOT / "work/recombine/results.jsonl"))
    ap.add_argument("--summary")
    args = ap.parse_args()
    out = Path(args.out)
    if args.summary:
        rows = [json.loads(l) for l in Path(args.summary).read_text(encoding="utf-8").splitlines() if l.strip()]
        print(summarise(rows))
        return 0
    seeds = load_seeds(args.arms)
    if args.only:
        seeds = {k: v for k, v in seeds.items() if any(o in k for o in args.only)}
    done = set()
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        done = {json.loads(l)["script"] for l in out.read_text(encoding="utf-8").splitlines() if l.strip()}
    tasks = [dict(script=k, seeds=v, pool=args.pool, draws=args.draws, manifest=args.manifest, library=args.library,
                  cache=str(ROOT / "work/replay/script_maps")) for k, v in sorted(seeds.items())
             if k not in done and len(v) >= 2]
    print(f"{len(tasks)} scripts ({sum(len(t['seeds']) for t in tasks)} seeds to verify), {args.workers} workers", flush=True)
    ctx = multiprocessing.get_context("spawn")
    allrows: list[dict] = []
    with ctx.Pool(args.workers) as pool, out.open("a", encoding="utf-8") as f:
        for i, rows in enumerate(pool.imap_unordered(work, tasks), 1):
            for r in rows:
                f.write(json.dumps(r) + "\n")
            f.flush()
            allrows += rows
            print(f"[{i}/{len(tasks)}] {rows[0]['script'][:44]:44s} " + (
                "ERROR " + rows[0]["error"][:80] if "error" in rows[0] else
                " ".join(f"{r['best_single']:.2f}->{r['recombined']:.2f}" for r in rows)), flush=True)
    print("\n" + summarise(allrows))
    return 0


if __name__ == "__main__":
    sys.exit(main())

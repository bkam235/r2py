"""Live smoke test of the post-plan harness on a handful of held-out scripts.

Runs the real pipeline (live LLM, pinned settings) with the trained `full` library, without
learning, into a scratch directory -- it touches nothing under work/heldout.  It answers:

  * does the agent use replace_entity, and is it refused / does it break the loop?
  * does the fail-closed review reject legitimate rewrites (LLM errors, unparseable verdicts)?
  * do shadow-fixer buckets, per-entity active_dims and graphics fingerprints reach the rows?
  * how long does a script take, and what did graphics score?

    python scripts/smoke_test.py --list              # show the selection, run nothing
    python scripts/smoke_test.py --check-llm         # one tiny request, then exit
    python scripts/smoke_test.py                     # the run (12 scripts, 10 min agent budget each)
    python scripts/smoke_test.py --n 6 --budget-s 300
    python scripts/smoke_test.py --workers 4         # scripts are independent; run them in parallel

Cost: every script makes several live LLM calls; the default selection is a few dollars at most,
but it is real spend.  Results: work/smoke/<timestamp>/{log.txt,rows.jsonl,summary.txt}.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import shutil
import sys
import tempfile
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env", override=True)  # as scripts/run_heldout.py does

# Scripts whose R run draws plots (from scripts/graphics_null_report.py on the held-out set).
PLOTTING = [
    "ggplot2__rd_example__aes_linetype_size_shape_Rd.R",
    "RColorBrewer__rd_example__ColorBrewer_Rd.R",
    "caret__rd_example__createDataPartition_Rd.R",
    "diagram__rd_example__diagram_Rd.R",
    "isoband__rd_example__isobands_Rd.R",
    "shape__rd_example__femmecol_Rd.R",
    "e1071__rd_example__hamming_window_Rd.R",
    "gtable__rd_example__gtable_show_layout_Rd.R",
    "pROC__rd_example__geom_polygon_auc_roc_Rd.R",
]


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, s):
        for st in self.streams:
            st.write(s)
        return len(s)

    def flush(self):
        for st in self.streams:
            st.flush()


def select(manifest: dict, pool: Path, n: int) -> list[str]:
    """The plotting scripts first, then the shortest other held-out scripts (cheapest to run)."""
    held = [e["script"] for e in manifest["heldout"]]
    chosen = [s for s in PLOTTING if s in held][:n]
    rest = sorted((s for s in held if s not in chosen),
                  key=lambda s: (next(pool.rglob(s)).stat().st_size, s))
    return chosen + rest[: max(0, n - len(chosen))]


def summarise(rows: list[dict], log: str) -> str:
    actions = Counter(re.findall(r"\[Agent\]\s+Step \d+: (\w+)", log))
    out = [f"scripts run: {len(rows)}  errors: {sum('error' in r for r in rows)}", ""]
    out.append(f"{'script':52s} {'score':>6s} {'gfx':>5s} {'min':>5s}  shadow  review-fail")
    for r in rows:
        gfx = r.get("by_effect", {}).get("graphics")
        shadow = Counter(f"{e['fixer'][:4]}:{e['bucket']}" for e in r.get("shadow_fixers", []))
        rv = {k: v for k, v in r.get("review_failures", {}).items() if v}
        out.append(f"{r['script'][:52]:52s} {r.get('score', float('nan')):6.3f} "
                   f"{'-' if gfx is None else f'{gfx:.2f}':>5s} {r['seconds'] / 60:5.1f}  "
                   f"{dict(shadow) or '-'}  {rv or '-'}")
    out += ["", f"agent actions: {dict(actions)}"]
    for label, pat in (("replace_entity refused", r"replace_entity refused"),
                       ("syntax errors", r"\[Agent\]\s+Syntax error"),
                       ("review PASSED", r"\[Review\]\s+PASSED"),
                       ("review FAILED", r"\[Review\]\s+FAILED"),
                       ("review unavailable", r"review unavailable"),
                       ("runtime SyntaxError dumps", r"runtime SyntaxError"),
                       ("budget exhausted", r"Wall-clock budget")):
        out.append(f"{label:28s} {len(re.findall(pat, log))}")
    ents = [e for r in rows for e in r.get("entities", [])]
    with_dims = sum(1 for e in ents if "active_dims" in e)
    out += ["", f"entity records: {len(ents)} ({with_dims} with active_dims)"]
    pinned = sum(1 for e in ents if e.get("active_dims") == [])
    out.append(f"entities with no active dimensions: {pinned}")
    gm = [r for r in rows if "graphics" in r.get("by_effect", {})]
    out.append(f"scripts with graphics scored: {len(gm)}"
               + (f"; mean {sum(r['by_effect']['graphics'] for r in gm) / len(gm):.2f}" if gm else ""))
    return "\n".join(out)


def run_parallel(args, scripts: list[str]) -> int:
    """One subprocess per shard (separate interpreters: the LLM pin and diagnostics are
    per-process), then merge their logs and rows into one summary."""
    import subprocess

    out = ROOT / "work" / "smoke" / datetime.now().strftime("%Y%m%d_%H%M%S")
    out.mkdir(parents=True)
    n = min(args.workers, len(scripts))
    print(f"smoke test: {len(scripts)} scripts on {n} workers -> {out}", flush=True)
    passthrough = (["--only", *args.only] if args.only else []) + ["--n", str(args.n), "--budget-s", str(args.budget_s), "--checkpoint", args.checkpoint,
                   "--manifest", args.manifest, "--workdir", args.workdir]
    procs = [subprocess.Popen([sys.executable, __file__, *passthrough, "--shard", f"{i}/{n}",
                               "--out", str(out)], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
             for i in range(n)]
    for i, p in enumerate(procs):
        p.wait()
        print(f"worker {i} exited with {p.returncode}", flush=True)

    rows = [json.loads(line) for f in sorted(out.glob("rows.w*.jsonl"))
            for line in f.read_text(encoding="utf-8").splitlines()]
    log = "\n".join(f.read_text(encoding="utf-8", errors="replace") for f in sorted(out.glob("log.w*.txt")))
    (out / "log.txt").write_text(log, encoding="utf-8")
    (out / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    text = summarise(rows, log)
    (out / "summary.txt").write_text(text, encoding="utf-8")
    print("\n" + text)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=12, help="number of scripts")
    ap.add_argument("--budget-s", type=float, default=600, help="agent wall-clock budget per script")
    ap.add_argument("--checkpoint", default="full")
    ap.add_argument("--manifest", default=str(ROOT / "experiments/heldout/manifest.json"))
    ap.add_argument("--workdir", default=str(ROOT / "work/heldout"), help="holds checkpoints/<name>")
    ap.add_argument("--only", nargs="+", metavar="SUBSTR",
                    help="run only held-out scripts whose name contains one of these")
    ap.add_argument("--workers", type=int, default=1, help="parallel worker processes")
    ap.add_argument("--shard", help=argparse.SUPPRESS)  # internal: "i/N", with --out
    ap.add_argument("--out", help=argparse.SUPPRESS)
    ap.add_argument("--list", action="store_true", help="print the selection and exit")
    ap.add_argument("--check-llm", action="store_true", help="one tiny live request, then exit")
    args = ap.parse_args()

    from r2py import heldout as ho

    manifest = ho.load_manifest(args.manifest)
    pool = ho._pool_path(manifest)
    if not pool.is_absolute():
        pool = ROOT / pool
    scripts = select(manifest, pool, args.n)
    if args.only:
        scripts = [e["script"] for e in manifest["heldout"] if any(o in e["script"] for o in args.only)]

    if args.list:
        for s in scripts:
            print(f"{'plots' if s in PLOTTING else 'other':6s} {s}")
        return 0
    if args.check_llm:
        ho.check_llm(manifest)
        return 0

    if args.workers > 1 and not args.shard:
        return run_parallel(args, scripts)
    shard = 0
    if args.shard:  # round-robin, so the slow plotting scripts (listed first) spread out
        shard, of = (int(x) for x in args.shard.split("/"))
        scripts = scripts[shard::of]

    cp_dir = Path(args.workdir) / "checkpoints" / args.checkpoint
    if not cp_dir.exists():
        sys.exit(f"no checkpoint at {cp_dir}")
    cfg = copy.deepcopy(manifest["protocol"]["translate"])
    cfg["agent_budget_s"] = args.budget_s

    out = Path(args.out) if args.out else ROOT / "work" / "smoke" / datetime.now().strftime("%Y%m%d_%H%M%S")
    out.mkdir(parents=True, exist_ok=True)
    tag = f".w{shard}" if args.shard else ""
    log_f = (out / f"log{tag}.txt").open("w", encoding="utf-8", buffering=1)
    real_stdout = sys.stdout
    sys.stdout = Tee(real_stdout, log_f)
    rows: list[dict] = []
    try:
        from r2py.library import PatternLibrary

        print(f"smoke test: {len(scripts)} scripts, checkpoint {args.checkpoint}, "
              f"agent budget {args.budget_s:.0f}s, harness {ho.harness_hash()} -> {out}")
        with ho.pinned_llm(cfg["model"]):
            for i, script in enumerate(scripts, 1):
                print(f"\n===== [{i}/{len(scripts)}] {script}", flush=True)
                row = {"script": script}
                started = time.monotonic()
                with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
                    shutil.copytree(cp_dir, Path(tmp) / "lib")
                    try:
                        r, entities = ho._translate_once(
                            next(pool.rglob(script)), out / "py" / (Path(script).stem + ".py"),
                            PatternLibrary(Path(tmp) / "lib"), cfg, learn=False)
                        rep = r.final_score_report
                        row.update(score=r.final_score, iterations=r.iterations,
                                   by_effect={k.value: v for k, v in rep.by_effect.items()} if rep else {},
                                   entities=entities)
                    except Exception as exc:
                        row["error"] = f"{type(exc).__name__}: {exc}"
                        print(f"  ERROR: {row['error']}")
                row.update(ho._drain_diagnostics())
                row["seconds"] = round(time.monotonic() - started, 1)
                rows.append(row)
                with (out / f"rows{tag}.jsonl").open("a", encoding="utf-8") as f:
                    f.write(json.dumps(row) + "\n")
    finally:
        sys.stdout = real_stdout
        log_f.close()

    if args.shard:
        return 0  # the parent merges and summarises
    text = summarise(rows, (out / "log.txt").read_text(encoding="utf-8", errors="replace"))
    (out / "summary.txt").write_text(text, encoding="utf-8")
    print("\n" + text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

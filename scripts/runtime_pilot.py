"""Pilot of the verified R-semantics runtime: can a small model reproduce R functions, judged by R? (roadmap step 7)

    python scripts/runtime_pilot.py candidates            # list what would be attempted
    python scripts/runtime_pilot.py run --limit 3         # try a few
    python scripts/runtime_pilot.py run --workers 6       # the whole candidate list
    python scripts/runtime_pilot.py summary

Candidates are derived from the pipeline's own data, not chosen by hand: (a) the functions of the entities that still
score below 0.9 in the best width-3 replay states (their own R function, in its package), and (b) the base/stats/utils
functions most called across the 316 corpus scripts, minus functions with side effects (I/O, printing, session state).
Results are appended to work/runtime/pilot/results.jsonl, accepted code to work/runtime/pilot/<pkg>__<name>.py.
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import multiprocessing
import pickle
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

OUT = ROOT / "work/runtime/pilot"
SIDE_EFFECTS = {
    "library", "require", "requireNamespace", "suppressPackageStartupMessages", "data", "plot", "print", "cat", "message",
    "warning", "stop", "try", "withAutoprint", "writeLines", "tempfile", "unlink", "system.file", "vignette", "set.seed",
    "Sys.time", "Sys.getenv", "Sys.setenv", "getRversion", "get", "stopifnot", "serialize", "Encoding", "str", "summary",
    "head", "lapply", "sapply", "vapply", "Map", "mapply", "do.call", "invisible", "identical", "predict", "glm", "lm",
    "data.frame", "matrix", "array", "list", "as.list", "as.data.frame", "as.matrix", "integer", "logical", "double",
    "cbind", "rbind", "nrow", "ncol", "t", "runif", "rnorm", "sample", "rgamma", "rpois", "rbinom",
}


def failing_entity_functions() -> list[tuple[str, str | None, str]]:
    """(function, package, source tag) for function-call entities that still score < 0.9 in the best width-3 replay states
    and name a function that exists in their package (variables and graphics helpers are dropped by that check)."""
    seen = {}
    for f in glob.glob(str(ROOT / "work/replay_v3/trajectories/*rewrite_w3*.jsonl")):
        recs = [json.loads(l) for l in open(f, encoding="utf-8")]
        script = recs[0]["script"]
        acc = [r for r in recs if r["kind"] == "accepted" and r.get("per_entity")]
        pkl = ROOT / "work/replay/script_maps" / (Path(script).stem + ".pkl")
        if not acc or not pkl.exists():
            continue
        best = max(acc, key=lambda r: r["aggregate"])
        sm = pickle.loads(pkl.read_bytes())
        pkg = script.split("__")[0]
        for eid, score in best["per_entity"].items():
            ent = sm.entities.get(eid)
            if ent is not None and score < 0.9 and ent.kind.value == "FunctionCall" and ent.name and ent.name not in SIDE_EFFECTS:
                seen.setdefault(ent.name, pkg)
    return [(n, p, "failing entity") for n, p in sorted(seen.items()) if function_exists(n, p)]


def function_exists(name: str, pkg: str) -> bool:
    import tempfile
    from r2py.stage0.sandbox.r_sandbox import RSandbox
    from r2py.types import EffectClass

    src = (f'ok <- tryCatch({{ suppressPackageStartupMessages(library({pkg})); '
           f'is.function(get("{name}", envir = asNamespace("{pkg}"), inherits = FALSE)) }}, error = function(e) FALSE)\n'
           'cat("@@", ok, "@@")\n')
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as t:
        out = RSandbox().run(src, workdir=Path(t), capture=frozenset({EffectClass.STDOUT}), timeout_s=60).stdout
    return "@@ TRUE @@" in out


def candidate_list() -> list[tuple[str, str | None, str]]:
    cands = [(n, p, t) for n, p, t in failing_entity_functions()]
    core = json.loads(Path(sys.argv[0]).parent.joinpath("..", "work/runtime/core_functions.json").read_text(encoding="utf-8")) \
        if (ROOT / "work/runtime/core_functions.json").exists() else []
    have = {n for n, _p, _t in cands}
    for name, _count, pkg in core:
        if name not in SIDE_EFFECTS and name not in have:
            cands.append((name, None, f"corpus frequency ({pkg})"))
    return cands


def task(args: tuple) -> dict:
    name, pkg, tag = args
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    from r2py import heldout as ho
    from r2py.runtime import propose

    man = ho.load_manifest(str(ROOT / "experiments/dev_run/manifest.json"))
    cfg = man["protocol"]["translate"]
    with ho.pinned_llm(cfg["model"], ho.llm_settings(man)):
        rec = propose.attempt(name, pkg, cfg["model"])
    rec["tag"] = tag
    propose.save(rec, OUT)
    return rec


def summarise(rows: list[dict]) -> str:
    if not rows:
        return "no results"
    c = collections.Counter(r["status"] for r in rows)
    out = [f"{len(rows)} functions: " + ", ".join(f"{k} {v}" for k, v in c.most_common())]
    done = [r for r in rows if r["status"] in ("passed", "failed")]
    if done:
        by_round = collections.Counter(r["rounds"] for r in rows if r["status"] == "passed")
        out.append(f"of the {len(done)} attempted, {c['passed']} pass all R-derived cases ({c['passed'] / len(done):.0%}); "
                   f"passing at round 1/2/3: {by_round.get(1, 0)}/{by_round.get(2, 0)}/{by_round.get(3, 0)}")
    for tag in sorted({r.get("tag", "").split(" (")[0] for r in rows}):
        sub = [r for r in done if r.get("tag", "").startswith(tag)]
        if sub:
            out.append(f"  {tag:18s} {sum(r['status'] == 'passed' for r in sub)}/{len(sub)} pass")
    out.append("failed: " + "; ".join(f"{r['function']} ({r.get('passed', 0)}/{r.get('total', 0)})" for r in rows if r["status"] == "failed"))
    out.append("no usable cases / errors: " + ", ".join(r["function"] for r in rows if r["status"] in ("no_cases", "error")))
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("candidates", "run", "summary"))
    ap.add_argument("--limit", type=int)
    ap.add_argument("--only", nargs="+")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    results = OUT / "results.jsonl"
    rows = [json.loads(l) for l in results.read_text(encoding="utf-8").splitlines() if l.strip()] if results.exists() else []
    if args.mode == "summary":
        print(summarise(rows))
        return 0
    cands = candidate_list()
    if args.only:
        cands = [c for c in cands if c[0] in args.only]
    if args.mode == "candidates":
        for n, p, t in cands:
            print(f"{(p + '::' if p else '') + n:40s} {t}")
        print(len(cands), "candidates")
        return 0
    done = {r["function"] for r in rows}
    todo = [c for c in cands if c[0] not in done][: args.limit]
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"{len(todo)} functions to try, {args.workers} workers", flush=True)
    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(args.workers) as pool, results.open("a", encoding="utf-8") as f:
        for i, rec in enumerate(pool.imap_unordered(task, todo), 1):
            slim = {k: v for k, v in rec.items() if k != "code"}
            f.write(json.dumps(slim, default=str) + "\n")
            f.flush()
            print(f"[{i}/{len(todo)}] {rec['function']:24s} {rec['status']:9s} rounds {rec.get('rounds')} "
                  f"{rec.get('passed', '-')}/{rec.get('total', '-')} {rec.get('error', '')[:60]}", flush=True)
    rows = [json.loads(l) for l in results.read_text(encoding="utf-8").splitlines() if l.strip()]
    print("\n" + summarise(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())

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

LOCATE = False     # --locate: tell the model where inside the R function its Python first departs
OUT = ROOT / "work/runtime/pilot_v2"   # the first pilot (work/runtime/pilot) validated serialised values; see the plan
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


def failing_entity_sites() -> list[dict]:
    """The real calls behind the failing-entity functions: (function, package, script R source, entity span)."""
    sites = {}
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
            span = getattr(ent, "source_span", None)
            if ent is not None and span is not None and score < 0.9 and ent.kind.value == "FunctionCall" and ent.name not in SIDE_EFFECTS:
                sites.setdefault(ent.name, {"function": ent.name, "package": pkg, "source": sm.source,
                                            "span": (span.start_line, span.end_line), "script": script})
    return list(sites.values())


def hard_task(args: tuple) -> dict:
    name, pkg, source, span, locate, out_dir = args
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    from r2py import heldout as ho
    from r2py.runtime import difftest, propose

    man = ho.load_manifest(str(ROOT / "experiments/dev_run/manifest.json"))
    cfg = man["protocol"]["translate"]
    mined = difftest.mine_cases(source, tuple(span), name, pkg)
    with ho.pinned_llm(cfg["model"], ho.llm_settings(man)):
        rec = propose.attempt(name, pkg, cfg["model"], rounds=8, attempts=4, mined=mined, source_limit=15000, budget_s=1800,
                              locate=locate)
    rec["tag"] = "failing entity (hard pass)"
    propose.save(rec, Path(out_dir))
    return rec


def fix_task(args: tuple) -> dict:
    """One candidate from the agent's fixes: mined real call + the fixed fragment as evidence."""
    name, pkg, source, span, hint_text, out_dir = args
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    from r2py import heldout as ho
    from r2py.runtime import difftest, propose

    man = ho.load_manifest(str(ROOT / "experiments/dev_run/manifest.json"))
    cfg = man["protocol"]["translate"]
    package = None if pkg in ("base", "stats", "utils", "") else pkg
    mined = difftest.mine_cases(source, tuple(span), name, package)
    with ho.pinned_llm(cfg["model"], ho.llm_settings(man)):
        rec = propose.attempt(name, package, cfg["model"], rounds=6, attempts=3, mined=mined, source_limit=15000, budget_s=1200,
                              locate=True, hint=hint_text)
    rec["tag"] = "agent fix"
    propose.save(rec, Path(out_dir))
    return rec


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
    out.append("failed: " + "; ".join(f"{r['function']} ({r.get('core_passed', r.get('passed', 0))}/{r.get('core_total', r.get('total', 0))})"
                                   for r in rows if r["status"] == "failed"))
    out.append("no usable cases / errors: " + ", ".join(r["function"] for r in rows if r["status"] in ("no_cases", "error")))
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("candidates", "run", "summary", "hard", "fixes", "purity"))
    ap.add_argument("--limit", type=int)
    ap.add_argument("--only", nargs="+")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--locate", action="store_true", help="hard mode: add the step-by-step locator to the repair messages")
    ap.add_argument("--out-dir", help="directory for results and accepted code (default work/runtime/pilot_v2)")
    ap.add_argument("--retry", action="store_true", help="only functions that did not pass before; results go to results_v2.jsonl")
    args = ap.parse_args()
    global OUT, LOCATE
    LOCATE = args.locate
    if args.out_dir:
        OUT = Path(args.out_dir)
    v1 = OUT / "results.jsonl"
    results = OUT / ("results_v2.jsonl" if args.retry else "results.jsonl")
    old = [json.loads(l) for l in v1.read_text(encoding="utf-8").splitlines() if l.strip()] if v1.exists() else []
    rows = [json.loads(l) for l in results.read_text(encoding="utf-8").splitlines() if l.strip()] if results.exists() else []
    if args.retry:   # a function's current record is its latest: v2 where it was retried, else v1
        latest = {r["function"]: r for r in old}
        latest.update({r["function"]: r for r in rows})
        rows_all = list(latest.values())
    else:
        rows_all = rows
    if args.mode == "summary":
        v2 = OUT / "results_v2.jsonl"
        latest = {r["function"]: r for r in old}
        if v2.exists():
            latest.update({json.loads(l)["function"]: json.loads(l) for l in v2.read_text(encoding="utf-8").splitlines() if l.strip()})
        print(summarise(list(latest.values())))
        return 0
    if args.mode == "purity":      # annotate accepted functions that are not values-from-values (see difftest.IMPURE)
        from r2py.runtime import difftest
        d = Path(args.out_dir) if args.out_dir else OUT
        recs = {f: json.loads(f.read_text(encoding="utf-8")) for f in sorted(d.glob("*.json"))}
        specs = [(r["function"], r.get("package")) for r in recs.values() if r.get("status") == "passed"]
        impure = difftest.impure_calls(specs)
        for f, r in recs.items():
            if r.get("status") == "passed":
                r["impure"] = impure.get(r["function"], [])
                f.write_text(json.dumps(r, indent=1, default=str), encoding="utf-8")
        print(f"{len(specs)} accepted functions; impure (excluded from the store): "
              + "; ".join(f"{k} {v}" for k, v in impure.items() if v))
        print("pure:", ", ".join(k for k, v in impure.items() if not v))
        return 0
    if args.mode == "fixes":
        from r2py.runtime import mine_fixes
        from r2py.runtime.store import RuntimeStore
        files = glob.glob(str(ROOT / "work/replay*/trajectories/*.jsonl")) + glob.glob(str(ROOT / "work/smoke/*/py/trajectories/*.jsonl"))
        fixes = mine_fixes.fixes_from_trajectories(files, ROOT / "work/replay/script_maps")
        known = {e.function for e in RuntimeStore(ROOT / "work/runtime/pilot_v2").entries.values()}
        by = mine_fixes.candidates(fixes, known)
        fx_out = ROOT / "work/runtime/pilot_v2_fixes"
        done = {json.loads(l)["function"] for l in (fx_out / "results.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}             if (fx_out / "results.jsonl").exists() else set()
        tasks = []
        for fn, fs in sorted(by.items()):
            best = max(fs, key=lambda f: (f.score_after - f.score_before))
            pkg = "base" if best.package in ("", "base", "stats", "utils") else best.package
            if fn in done or (args.only and fn not in args.only) or not function_exists(fn, pkg):
                continue
            tasks.append((fn, pkg, best.r_source, best.span, mine_fixes.hint(best), str(fx_out)))
        tasks = tasks[: args.limit]
        fx_out.mkdir(parents=True, exist_ok=True)
        print(f"{len(by)} candidate functions from the agent's fixes, {len(tasks)} to try", flush=True)
        ctx = multiprocessing.get_context("spawn")
        with ctx.Pool(args.workers) as pool, (fx_out / "results.jsonl").open("a", encoding="utf-8") as f:
            for i, rec in enumerate(pool.imap_unordered(fix_task, tasks), 1):
                f.write(json.dumps({k: v for k, v in rec.items() if k != "code"}, default=str) + "\n")
                f.flush()
                print(f"[{i}/{len(tasks)}] {rec['function']:26s} {rec['status']:9s} mined {rec.get('n_mined')} "
                      f"core {rec.get('core_passed', '-')}/{rec.get('core_total', '-')} attempt {rec.get('attempt', '-')} round {rec.get('rounds')} "
                      f"{rec.get('error', '')[:60]}", flush=True)
        return 0
    if args.mode == "hard":
        sites = [x for x in failing_entity_sites() if function_exists(x["function"], x["package"])]
        if args.only:
            sites = [x for x in sites if x["function"] in args.only]
        hard = OUT / "hard_results.jsonl"
        print(f"{len(sites)} failing-entity functions: {[x['function'] for x in sites]}", flush=True)
        ctx = multiprocessing.get_context("spawn")
        with ctx.Pool(min(args.workers, max(1, len(sites)))) as pool, hard.open("a", encoding="utf-8") as f:
            for rec in pool.imap_unordered(hard_task, [(x["function"], x["package"], x["source"], x["span"], args.locate, str(OUT)) for x in sites]):
                f.write(json.dumps({k: v for k, v in rec.items() if k != "code"}, default=str) + "\n")
                f.flush()
                print(f"{rec['function']:22s} {rec['status']:9s} mined {rec.get('n_mined')} core {rec.get('core_passed', '-')}/{rec.get('core_total', '-')} "
                      f"attempt {rec.get('attempt', '-')} round {rec.get('rounds')} {rec.get('error', '')[:60]}", flush=True)
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
    if args.retry:
        passed_before = {r["function"] for r in old if r["status"] == "passed"}
        todo = [c for c in cands if c[0] not in passed_before and c[0] not in done][: args.limit]
    else:
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
                  f"core {rec.get('core_passed', rec.get('passed', '-'))}/{rec.get('core_total', rec.get('total', '-'))} "
                  f"(attempt {rec.get('attempt', '-')}) {rec.get('error', '')[:60]}", flush=True)
    rows = [json.loads(l) for l in results.read_text(encoding="utf-8").splitlines() if l.strip()]
    latest = {r["function"]: r for r in old}
    latest.update({r["function"]: r for r in rows})
    print("\n" + summarise(list(latest.values())))
    return 0


if __name__ == "__main__":
    sys.exit(main())

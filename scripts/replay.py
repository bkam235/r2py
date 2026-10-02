"""Paired replay: compare agent policies from IDENTICAL frozen starting states (Stage 9d).

Whole-script arms cannot resolve small effects: the seed stage differs between arms in about half the
scripts, and per-script run-to-run SD is ~0.2.  Here every policy starts from the same state (a logged
seed translation and its verification) and only the agent loop differs, so what is measured is the agent.
Each (state, policy) is run several times, which also measures the noise of the agent itself.

    python scripts/replay.py --arms work/smoke/20261001_112951 work/smoke/20261001_140509 work/smoke/20261001_165951 \\
        --policies rewrite entity_esc --samples 3 --workers 6

States: for each script, the best seed found across ``--arms`` (trajectory logs); scripts whose best seed
already reaches ``--max-start`` are skipped (nothing for the agent to do).
Policies: rewrite_w3 (three independent rewrite loops, best wins) | rewrite (the default loop) | entity_esc (entity repair, escalating to a full rewrite after two
misses) | entity_only (entity repair, never escalating).
Results: ``--out`` JSONL, appended as runs finish (resumable: finished (state, policy, sample) are skipped).
"""
from __future__ import annotations

import argparse
import copy
import json
import multiprocessing
import pickle
import shutil
import statistics as st
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

POLICIES = {
    "rewrite": dict(entity_repair=False, escalate_after=None),
    "entity_esc": dict(entity_repair=True, escalate_after=2),
    "entity_only": dict(entity_repair=True, escalate_after=10 ** 6),
    "rewrite_w3": dict(entity_repair=False, escalate_after=None, width=3),   # three independent loops, best wins
}


def best_states(arms: list[str], max_start: float) -> dict[str, dict]:
    """script -> {source, label, aggregate, hash} of the highest-scoring logged seed."""
    from r2py.harness import trajectory

    best: dict[str, dict] = {}
    for arm in arms:
        for f in sorted((Path(arm) / "py" / "trajectories").glob("*.jsonl")):
            recs = trajectory.read(f)
            name = recs[0]["script"]
            for r in recs:
                if r["kind"] == "seed" and r.get("source"):
                    if name not in best or r["aggregate"] > best[name]["aggregate"]:
                        best[name] = {"source": r["source"], "label": r["label"],
                                      "aggregate": r["aggregate"], "hash": r["source_hash"]}
    return {n: s for n, s in best.items() if s["aggregate"] < max_start}


def _script_map(name: str, manifest, cache: Path):
    """The analysed script, cached on disk: analysis runs R and takes about a minute."""
    from r2py import heldout as ho
    from r2py.stage1 import analyze

    f = cache / (Path(name).stem + ".pkl")
    if f.exists():
        return pickle.loads(f.read_bytes())
    pool = ho._pool_path(manifest)
    if not pool.is_absolute():
        pool = ROOT / pool
    sm = analyze(next(pool.rglob(name)))
    sm.ast_root = None   # a tree-sitter node (not picklable); only analysis itself reads it
    cache.mkdir(parents=True, exist_ok=True)
    tmp = f.with_suffix(f".{multiprocessing.current_process().pid}.tmp")
    tmp.write_bytes(pickle.dumps(sm))
    tmp.replace(f)
    return sm


def run_one(task: dict) -> dict:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    from r2py import heldout as ho
    from r2py.harness import trajectory
    from r2py.harness.agent import drain_agent_stats, reason_wide
    from r2py.harness.audit import format_audit_for_agent, static_audit
    from r2py.harness.tools import HarnessTools
    from r2py.library import PatternLibrary
    from r2py.stage1.runner import strip_r_guards

    manifest = ho.load_manifest(task["manifest"])
    cfg = manifest["protocol"]["translate"]
    row = {k: task[k] for k in ("script", "policy", "sample", "label", "start_hash")}
    started = time.monotonic()
    out_dir = Path(task["out_dir"])
    try:
        with ho.pinned_llm(cfg["model"], ho.llm_settings(manifest)):
            sm = _script_map(task["script"], manifest, Path(task["cache"]))
            with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
                shutil.copytree(Path(task["library"]), Path(tmp) / "lib")
                lib = PatternLibrary(Path(tmp) / "lib")
                def new_harness():
                    return HarnessTools(sm, lib, model=cfg["model"], data_compare=cfg["data_compare"],
                                        timeout_s=cfg["timeout_s"],
                                        sidecar_filename=f"{Path(task['script']).stem}.r2py_data.json")
                harness = new_harness()
                trajectory.begin(out_dir / "trajectories" / f"{Path(task['script']).stem}.{task['policy']}.{task['sample']}.jsonl",
                                 script=task["script"], policy=task["policy"], sample=task["sample"])
                harness.note_reference(task["source"])
                start_report = harness.verify(task["source"])
                row["start_score"] = round(start_report.aggregate, 4)
                row["start_exit"] = start_report.py_exit_code
                audit = ""
                try:
                    findings = static_audit(strip_r_guards(sm.source or ""), task["source"], sm, model=cfg["model"])
                    audit = format_audit_for_agent(findings) if findings else ""
                except Exception:
                    pass
                drain_agent_stats()
                policy = dict(POLICIES[task["policy"]])
                width = policy.pop("width", 1)
                result = reason_wide(
                    [harness] + [new_harness() for _ in range(width - 1)],
                    current_source=task["source"], score_report=start_report, script_map=sm, model=cfg["model"],
                    max_steps=cfg["max_iters"], score_threshold=cfg["score_threshold"], max_stalls=cfg["max_stalls"],
                    budget_s=task["budget_s"], audit_feedback=audit, replace_entity=False, **policy)
                final = result[1].aggregate if result else start_report.aggregate
                row.update(final_score=round(final, 4), improved=bool(result and final > start_report.aggregate + 1e-9),
                           final_exit=(result[1].py_exit_code if result else start_report.py_exit_code))
                row["agent"] = drain_agent_stats()
                trajectory.end(final_score=row["final_score"])
    except Exception as exc:
        row["error"] = f"{type(exc).__name__}: {exc}"[:300]
    row["seconds"] = round(time.monotonic() - started, 1)
    return row


def summarise(rows: list[dict]) -> str:
    rows = [r for r in rows if "final_score" in r]
    if not rows:
        return "no finished runs"
    policies = sorted({r["policy"] for r in rows})
    states = sorted({r["script"] for r in rows})
    by = {(r["script"], r["policy"]): [] for r in rows}
    for r in rows:
        by[(r["script"], r["policy"])].append(r)
    lines = [f"{len(rows)} runs over {len(states)} frozen states, policies {policies}", ""]
    lines.append(f"{'policy':12s} {'runs':>5s} {'mean final':>11s} {'mean gain':>10s} {'P(improve)':>11s} {'P(final>=0.9)':>14s} {'min sd within state':>20s}")
    for p in policies:
        rs = [r for r in rows if r["policy"] == p]
        sds = [st.pstdev([x["final_score"] for x in by[(s, p)]]) for s in states if len(by.get((s, p), [])) > 1]
        lines.append(f"{p:12s} {len(rs):5d} {st.mean(r['final_score'] for r in rs):11.3f} "
                     f"{st.mean(r['final_score'] - r['start_score'] for r in rs):10.3f} "
                     f"{sum(r['improved'] for r in rs) / len(rs):11.0%} {sum(r['final_score'] >= 0.9 for r in rs) / len(rs):14.0%} "
                     f"{(st.mean(sds) if sds else float('nan')):20.3f}")
    base = "rewrite" if "rewrite" in policies else policies[0]
    for p in policies:
        if p == base:
            continue
        diffs = []
        for s in states:
            a, b = by.get((s, base)), by.get((s, p))
            if a and b:
                diffs.append(st.mean(x["final_score"] for x in b) - st.mean(x["final_score"] for x in a))
        if len(diffs) > 1:
            m, sd = st.mean(diffs), st.stdev(diffs)
            se = sd / len(diffs) ** 0.5
            try:
                from scipy.stats import wilcoxon
                pv = float(wilcoxon(diffs).pvalue) if any(abs(d) > 1e-9 for d in diffs) else 1.0
            except ImportError:
                pv = float("nan")
            lines.append(f"\n{p} - {base}, paired by state (mean over samples): {m:+.3f}  SE {se:.3f}  "
                         f"states {len(diffs)}  better/worse/tied {sum(d > 0.01 for d in diffs)}/"
                         f"{sum(d < -0.01 for d in diffs)}/{sum(abs(d) <= 0.01 for d in diffs)}  Wilcoxon p={pv:.3f}")
    return "\n".join(lines)


def main() -> int:
    from r2py.keepawake import keep_awake
    keep_awake()   # an idle laptop freezes background jobs (Modern Standby)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arms", nargs="+", required=True)
    ap.add_argument("--policies", nargs="+", default=["rewrite", "entity_esc"], choices=sorted(POLICIES))
    ap.add_argument("--samples", type=int, default=3)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--max-start", type=float, default=0.9, help="skip states whose seed already reaches this")
    ap.add_argument("--only", nargs="+", help="substrings of script names")
    ap.add_argument("--budget-s", type=float, default=1200)
    ap.add_argument("--manifest", default=str(ROOT / "experiments/dev_run/manifest.json"))
    ap.add_argument("--library", default=str(ROOT / "work/dev_run/checkpoints/empty"))
    ap.add_argument("--out", default=str(ROOT / "work/replay/results.jsonl"))
    ap.add_argument("--summary-only", action="store_true")
    args = ap.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    done = []
    if out.exists():
        done = [json.loads(l) for l in out.read_text(encoding="utf-8").splitlines() if l.strip()]
    if args.summary_only:
        print(summarise(done))
        return 0

    states = best_states(args.arms, args.max_start)
    if args.only:
        states = {n: s for n, s in states.items() if any(o in n for o in args.only)}
    finished = {(r["script"], r["policy"], r["sample"]) for r in done if "final_score" in r}
    tasks = []
    # sample-major order: every state/policy gets sample 0 before any gets sample 1, so an early stop
    # still leaves a balanced design
    for sample in range(args.samples):
        for name, s in sorted(states.items()):
            for policy in args.policies:
                if (name, policy, sample) in finished:
                    continue
                tasks.append(dict(script=name, policy=policy, sample=sample, source=s["source"], label=s["label"],
                                  start_hash=s["hash"], manifest=args.manifest, library=args.library,
                                  cache=str(ROOT / "work/replay/script_maps"), out_dir=str(out.parent),
                                  budget_s=args.budget_s))
    listing = ", ".join("%s(%.2f)" % (n[:18], s["aggregate"]) for n, s in sorted(states.items()))
    print(f"{len(states)} frozen states: {listing}")
    print(f"{len(tasks)} runs to do ({len(finished)} already finished), {args.workers} workers", flush=True)

    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(args.workers) as pool, out.open("a", encoding="utf-8") as f:
        for i, row in enumerate(pool.imap_unordered(run_one, tasks), 1):
            f.write(json.dumps(row) + "\n")
            f.flush()
            done.append(row)
            print(f"[{i}/{len(tasks)}] {row['script'][:36]:36s} {row['policy']:11s} s{row['sample']}: "
                  + (f"{row['start_score']:.2f} -> {row['final_score']:.2f} ({row['seconds'] / 60:.0f} min)"
                     if "final_score" in row else f"ERROR {row.get('error', '')[:80]}"), flush=True)
    print("\n" + summarise(done))
    return 0


if __name__ == "__main__":
    sys.exit(main())

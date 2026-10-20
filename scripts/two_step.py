"""Does step 2 use step 1's outcome better in one conversation? (registered 2026-10-19, before the run)

Per training-pool state and sample, the production loop (width 1, strict acceptance, no audit) runs two steps three
times, with step 1 shared:
  A  fresh (production): 2 steps; step 1's model answer and review verdicts are recorded;
  B  step 1 only, replayed (no model call): the best program after step 1;
  C  conversation (`reason(converse=True)`): 2 steps, step 1 replayed, step 2 continues step 1's conversation.
Primary: P(step 2 improves on the best after step 1), fresh vs conversation, paired per state.

    python scripts/two_step.py run --samples 2 --workers 8
    python scripts/two_step.py summary
"""
from __future__ import annotations

import argparse
import json
import multiprocessing
import random
import shutil
import statistics as st
import sys
import tempfile
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
OUT = ROOT / "work/two_step"


def run_one(task: dict) -> dict:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    import replay
    from r2py import heldout as ho
    from r2py.harness import agent
    from r2py.harness import objective as obj
    from r2py.harness.tools import HarnessTools
    from r2py.library import PatternLibrary

    row = {"script": task["script"], "sample": task["sample"]}
    started = time.monotonic()
    manifest = ho.load_manifest(ROOT / "experiments/dev_run/manifest.json")
    cfg = manifest["protocol"]["translate"]
    real_call, real_review = agent._llm.call, agent.review_translation
    try:
        with ho.pinned_llm(cfg["model"], ho.llm_settings(manifest)), tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            sm = replay._script_map(task["script"], manifest, replay.TRAIN_MAPS)
            shutil.copytree(ROOT / "work/dev_run/checkpoints/empty", Path(tmp) / "lib")
            lib = PatternLibrary(Path(tmp) / "lib")

            def harness():
                return HarnessTools(sm, lib, model=cfg["model"], data_compare=cfg["data_compare"], timeout_s=cfg["timeout_s"],
                                    sidecar_filename=f"{Path(task['script']).stem}.r2py_data.json")
            h0 = harness()
            h0.note_reference(task["source"])
            start = h0.verify(task["source"])
            row.update(start=round(start.aggregate, 4), start_exit=start.py_exit_code)

            # step 1's model answers and review verdicts, in order (the loop records its current step in agent._ctx)
            rec = {"calls": [], "reviews": []}
            state = {"mode": "record", "c": 0, "r": 0, "steps": set()}
            in_step1 = lambda: agent._ctx.get("step") == 1      # noqa: E731

            def call(messages, system, **kw):
                state["steps"].add(agent._ctx.get("step"))
                if state["mode"] == "replay" and in_step1():
                    out = rec["calls"][state["c"]]
                    state["c"] += 1
                else:
                    try:
                        out = real_call(messages, system, **kw)
                    except agent.TruncatedResponseError as exc:
                        out = exc
                    if state["mode"] == "record" and in_step1():
                        rec["calls"].append(out)
                if isinstance(out, Exception):
                    raise out
                return out

            def review(*a, **kw):
                if state["mode"] == "replay" and in_step1():
                    v = rec["reviews"][state["r"]]
                    state["r"] += 1
                    return v
                v = real_review(*a, **kw)
                if state["mode"] == "record" and in_step1():
                    rec["reviews"].append(v)
                return v

            agent._llm.call, agent.review_translation = call, review
            common = dict(script_map=sm, model=cfg["model"], score_threshold=cfg["score_threshold"],
                          max_stalls=cfg["max_stalls"], budget_s=2400, replace_entity=False, entity_repair=False)

            def run(mode, steps, converse):
                state.update(mode=mode, c=0, r=0, steps=set())
                agent._ctx.clear()
                h = harness()
                res = agent.reason(task["source"], start, h, max_steps=steps, converse=converse, **common)
                stats = agent.drain_agent_stats()
                return (res[1] if res else start), (2 in state["steps"]), stats

            fresh, ran_fresh, stats_fresh = run("record", 2, False)
            best1, _, stats1 = run("replay", 1, False)
            conv, ran_conv, stats_conv = run("replay", 2, True)
            row.update(best1=round(best1.aggregate, 4), best1_exit=best1.py_exit_code,
                       fresh=round(fresh.aggregate, 4), fresh_exit=fresh.py_exit_code,
                       conv=round(conv.aggregate, 4), conv_exit=conv.py_exit_code,
                       step1_improved=obj.better(best1, start),
                       fresh_improved=obj.better(fresh, best1), conv_improved=obj.better(conv, best1),
                       step2_ran=(ran_fresh and ran_conv),
                       conversation_turns=stats_conv.get("outcome", {}).get("conversation_turn", 0))
    except Exception as exc:
        row["error"] = f"{type(exc).__name__}: {exc}"[:300]
    finally:
        agent._llm.call, agent.review_translation = real_call, real_review
    row["seconds"] = round(time.monotonic() - started, 1)
    return row


def run(samples: int, workers: int) -> None:
    import replay
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / "results.jsonl"
    done = {(r["script"], r["sample"]) for r in map(json.loads, out.open(encoding="utf-8")) if "error" not in r} if out.exists() else set()
    states = replay.training_states()
    tasks = [{"script": n, "sample": s, "source": v["source"]} for s in range(samples) for n, v in sorted(states.items())
             if (n, s) not in done]
    print(f"{len(tasks)} trials, {workers} workers", flush=True)
    with multiprocessing.get_context("spawn").Pool(workers) as pool, out.open("a", encoding="utf-8") as f:
        for i, row in enumerate(pool.imap_unordered(run_one, tasks), 1):
            f.write(json.dumps(row) + "\n")
            f.flush()
            print(f"[{i}/{len(tasks)}] {row['script'][:40]} s{row['sample']}: "
                  + (f"start {row['start']:.3f} step1 {row['best1']:.3f} | fresh {row['fresh']:.3f} conv {row['conv']:.3f}"
                     if "error" not in row else f"ERROR {row['error'][:100]}"), flush=True)


def summary() -> None:
    rows = [json.loads(l) for l in (OUT / "results.jsonl").open(encoding="utf-8")]
    ok = [r for r in rows if "error" not in r]
    ran = [r for r in ok if r["step2_ran"]]
    print(f"{len(rows)} trials, errors {len(rows) - len(ok)}, step 2 ran in {len(ran)}; "
          f"conversation turns used in {sum(r['conversation_turns'] > 0 for r in ran)}")
    rng = random.Random(0)
    for label, sel in (("all", lambda r: True), ("running starts", lambda r: r["start_exit"] == 0),
                       ("crashing starts", lambda r: r["start_exit"] != 0)):
        rs = [r for r in ran if sel(r)]
        if not rs:
            continue
        print(f"\n{label} ({len(rs)} trials): step 1 improved {st.mean(r['step1_improved'] for r in rs):.3f}; "
              f"step 2 improved: fresh {st.mean(r['fresh_improved'] for r in rs):.3f}, "
              f"conversation {st.mean(r['conv_improved'] for r in rs):.3f}")
        for metric, f in (("P(step 2 improves)", lambda r, a: float(r[f"{a}_improved"])),
                          ("step-2 gain", lambda r, a: max(0.0, r[a] - r["best1"]) if r[f"{a}_improved"] else 0.0)):
            per = defaultdict(list)
            for r in rs:
                per[r["script"]].append(f(r, "conv") - f(r, "fresh"))
            d = [st.mean(v) for v in per.values()]
            b = sorted(st.mean(rng.choice(d) for _ in d) for _ in range(5000))
            print(f"  conversation - fresh, {metric}: {st.mean(d):+.4f} [{b[125]:+.4f}, {b[4874]:+.4f}]  ({len(d)} states)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "summary"])
    ap.add_argument("--samples", type=int, default=2)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    run(a.samples, a.workers) if a.cmd == "run" else summary()

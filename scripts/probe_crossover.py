"""Probe crossover at the stall-2 step (hypothesis (b), 2026-11-13): does DeepSeek V4.1 Flash ask better probe
questions than GLM 5.3 Flash, or does it only make better use of the answers?

The saved stall-2 chains of `model-screen-stall2` (`stall2_continue.chains()`), a fixed subset chosen by seed before
any result, are continued as in that screen (width 1, free probes in the script's R state, start at stall 2, at most 8
steps), in four arms: prober {glm, ds} x rewriter {glm, ds}. The prober answers every agent turn and so decides when
to probe, what to ask, and when to stop; whenever its answer is a rewrite (or a replace_entity), the same messages go
to the rewriter, and the rewriter's answer replaces it (in the conversation too). If the rewriter answers with a
probe or "done" instead, it is asked once more with a one-off line (NUDGE, not kept in the conversation); if it still
declines, the prober's own rewrite stands (logged), so every probe is the prober's. Diagonal arms run the same way (the
rewrite is resampled from the same model), so every arm pays the same extra call per rewrite. The review, the audit and
the entity mapping stay on Gemma. Each routed turn is logged to the trajectory (`route` records), and every probe's
expression and result (`probe` records, harness telemetry since 2026-11-13).

Analysis (`analyze`): per chain gain = final - score at the stall-2 point; per state the mean over its chains; per arm
the mean over states. Effects, bootstrap over states: prober (ds - glm, averaged over both rewriters), rewriter (ds -
glm, averaged over both probers), interaction. Descriptive, per prober: probes per chain, share of probes that error,
share that name a failing entity of the program they probe, result length; and 25 probes per prober to read.

    python scripts/probe_crossover.py run --workers 6 --budget 5 [--per-state 2] [--limit 2 --out work/x]
    python scripts/probe_crossover.py analyze [--out work/probe_crossover]
"""
from __future__ import annotations

import argparse
import collections
import json
import multiprocessing
import random
import re
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import replay  # noqa: E402
import stall2_continue as s2  # noqa: E402

OUT = ROOT / "work/probe_crossover"
MODELS = {"glm": ("openrouter:z-ai/glm-5.3-flash", "novita/fp8"),
          "ds": ("openrouter:deepseek/deepseek-v4.1-flash-1017", "deepinfra/fp8")}
ARMS = {f"px_{p}_{r}": (p, r) for p in MODELS for r in MODELS}   # px_<prober>_<rewriter>
SEED = 20261113
NUDGE = ("Write your rewrite now: answer with ACTION: rewrite and the complete Python program. "
         "Do not probe and do not stop.")

for _arm, (_p, _r) in ARMS.items():   # a worker that unpickles run_task imports this module: policies exist there too
    replay.POLICIES[_arm] = dict(replay.POLICIES[f"stall2_ps_{ {'glm': 'glmflash', 'ds': 'dsflash'}[_p]}"])


_ARM: dict = {}   # this process's current (prober, rewriter); the wrappers are installed once per process


def _route(prober: str, rewriter: str):
    """Set this process's arm; on first use, install the routing wrapper on `llm.call` (agent turns only) and the
    rewriter's provider pin. A pool worker runs many tasks: wrapping again per task would nest the wrappers."""
    _ARM.update(prober=prober, rewriter=rewriter)
    if _ARM.get("installed"):
        return
    _ARM["installed"] = True
    from r2py import heldout as ho
    from r2py.harness import agent, trajectory
    from r2py.stage2 import llm
    from r2py.stage2.llm import TruncatedResponseError

    orig_call, orig_pinned = llm.call, ho.pinned_llm

    def pinned(model, settings):
        r_model = MODELS[_ARM["rewriter"]][0]
        name = r_model.removeprefix("openrouter:")
        settings = {**settings,
                    "provider_by_model": {**(settings.get("provider_by_model") or {}),
                                          name: {"only": [MODELS[_ARM["rewriter"]][1]], "allow_fallbacks": False}},
                    "extra_by_model": {**(settings.get("extra_by_model") or {}),
                                       name: {"reasoning": {"max_tokens": 8000}}}}
        return orig_pinned(model, settings)

    def call(messages, system, *, model=None, **kw):
        prober, rewriter = _ARM["prober"], _ARM["rewriter"]
        p_model, r_model = MODELS[prober][0], MODELS[rewriter][0]
        if model != p_model:                       # review, audit, mapping: untouched
            return orig_call(messages, system, model=model, **kw) if model else orig_call(messages, system, **kw)
        prefix = messages[-1]["content"] if messages and messages[-1].get("role") == "assistant" else ""
        try:
            raw, truncated = orig_call(messages, system, model=p_model, **kw), None
        except TruncatedResponseError as exc:
            raw, truncated = exc.partial_text, exc
        a = agent._parse_action(prefix + raw)
        act = a.get("action") if a else None
        rec = dict(agent._ctx)
        rec.pop("source", None)
        if act in ("rewrite", "replace_entity"):
            # The rewriter writes this turn. Given the prober's conversation it may answer with a probe or "done"
            # instead: then it is asked once more with a one-off line (not kept in the conversation); if it still
            # declines, the prober's own rewrite stands. Probes therefore always come from the prober.
            tried = []
            for nudge in (False, True):
                if nudge and prefix:
                    break
                msgs = messages + [{"role": "user", "content": NUDGE}] if nudge else messages
                try:
                    r_raw, r_trunc = orig_call(msgs, system, model=r_model, **kw), None
                except TruncatedResponseError as exc:
                    r_raw, r_trunc = exc.partial_text, exc
                ra = agent._parse_action(prefix + r_raw)
                tried.append(ra.get("action") if ra else None)
                if tried[-1] in ("rewrite", "replace_entity"):
                    trajectory.log("route", prober_action=act, written_by=rewriter, rewriter_tries=tried,
                                   prefill=bool(prefix), prober_truncated=truncated is not None, **rec)
                    if r_trunc is not None:
                        raise r_trunc
                    return r_raw
            trajectory.log("route", prober_action=act, written_by=prober, rewriter_declined=tried,
                           prefill=bool(prefix), prober_truncated=truncated is not None, **rec)
        else:
            trajectory.log("route", prober_action=act, written_by=prober, prefill=bool(prefix),
                           prober_truncated=truncated is not None, **rec)
        if truncated is not None:
            raise truncated
        return raw

    llm.call = call
    ho.pinned_llm = pinned


def run_task(task: dict) -> dict:
    _route(*ARMS[task["policy"]])
    return replay.run_one(task)


def chains(per_state: int | None) -> list:
    """The reached stall-2 chains, at most `per_state` per state (chosen by SEED, before any result)."""
    by_state = collections.defaultdict(list)
    for k, c in sorted(s2.chains().items()):
        if c["reached"]:
            by_state[k[0]].append((k, c))
    rng = random.Random(SEED)
    out = []
    for s in sorted(by_state):
        cs = by_state[s]
        out += cs if per_state is None else rng.sample(cs, min(per_state, len(cs)))
    return out


def run(workers: int, budget: float, reserve: float, per_state: int | None, arms, out_dir: Path, limit=None) -> None:
    from expkit import RunGuard
    from r2py.keepawake import keep_awake
    keep_awake()   # machine sleep invalidates rows
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "results.jsonl"
    done = {(r["script"], r["policy"], r["sample"]) for r in map(json.loads, out.open(encoding="utf-8"))
            if "final_score" in r and not r.get("invalid")} if out.exists() else set()
    tasks = []
    for (script, run_label, b), c in chains(per_state)[:limit]:
        for arm in arms:
            key = f"{run_label}.{b}"
            if (script, arm, key) not in done:
                tasks.append(dict(script=script, policy=arm, sample=key, source=c["source"], label="stall2",
                                  start_hash=c["hash"], manifest=str(ROOT / "experiments/dev_run/manifest.json"),
                                  library=str(ROOT / "work/dev_run/checkpoints/empty"), runtime_dir=None,
                                  cache=str(replay.TRAIN_MAPS), out_dir=str(out_dir), budget_s=1200))
    random.Random(SEED).shuffle(tasks)   # arms interleaved: a budget stop or provider outage hits all arms alike
    print(f"{len(tasks)} continuations to run, {workers} workers", flush=True)
    ctx = multiprocessing.get_context("spawn")
    with RunGuard(out_dir, budget=budget, reserve=reserve) as guard, ctx.Pool(workers) as pool, \
            out.open("a", encoding="utf-8") as f:
        for i, row in enumerate(pool.imap_unordered(run_task, tasks), 1):
            row = guard.annotate(row)
            f.write(json.dumps(row) + "\n")
            f.flush()
            print(f"[{i}/{len(tasks)}] {row['script'][:36]:36s} {row['policy']:10s} {row['sample']}: "
                  + (f"{row['start_score']:.3f} -> {row['final_score']:.3f}, {row['llm_steps']} calls"
                     if "final_score" in row else f"ERROR {row.get('error', '')[:80]}"), flush=True)


# ------------------------------------------------------------------------------------------------ analysis

def _boot(vals: list, n: int = 10000) -> tuple:
    rng = random.Random(0)
    d = sorted(st.mean(rng.choices(vals, k=len(vals))) for _ in range(n))
    return st.mean(vals), d[int(.025 * n)], d[int(.975 * n)], sum(x > 0 for x in d) / n


def _failing_names(per_entity: dict) -> set:
    return {re.sub(r"_\d+$", "", e) for e, v in (per_entity or {}).items() if v < 1.0}


def analyze(out_dir: Path) -> None:
    rows = {}
    for r in map(json.loads, (out_dir / "results.jsonl").open(encoding="utf-8")):
        if "final_score" in r and not r.get("invalid"):
            rows[(r["script"], r["policy"], r["sample"])] = r
    gain = collections.defaultdict(lambda: collections.defaultdict(list))   # arm -> state -> chain gains
    for (script, arm, _), r in rows.items():
        gain[arm][script].append(float(r["final_score"]) - float(r["start_score"]))
    per = {arm: {s: st.mean(v) for s, v in g.items()} for arm, g in gain.items()}
    states = sorted(set.intersection(*(set(per.get(a, {})) for a in ARMS)))
    print(f"states with all four arms: {len(states)}")
    for arm in ARMS:
        n = sum(len(gain[arm][s]) for s in states)
        print(f"  {arm:10s} chains {n:3d}  mean gain {st.mean(per[arm][s] for s in states):+.4f}")
    g = {a: [per[a][s] for s in states] for a in ARMS}
    eff = {"prober (ds - glm)": [(g["px_ds_glm"][i] + g["px_ds_ds"][i] - g["px_glm_glm"][i] - g["px_glm_ds"][i]) / 2
                                 for i in range(len(states))],
           "rewriter (ds - glm)": [(g["px_glm_ds"][i] + g["px_ds_ds"][i] - g["px_glm_glm"][i] - g["px_ds_glm"][i]) / 2
                                   for i in range(len(states))],
           "interaction": [g["px_ds_ds"][i] - g["px_ds_glm"][i] - g["px_glm_ds"][i] + g["px_glm_glm"][i]
                           for i in range(len(states))]}
    for k, v in eff.items():
        m, lo, hi, p = _boot(v)
        print(f"  {k:20s} {m:+.4f} [{lo:+.4f}, {hi:+.4f}]  P(> 0) {p:.2f}")

    # probe questions, per prober (all arms of that prober)
    probes = collections.defaultdict(list)
    for f in sorted((out_dir / "trajectories").glob("*.jsonl")):
        recs = [json.loads(l) for l in f.open(encoding="utf-8")]
        recs = recs[max(i for i, r in enumerate(recs) if r["kind"] == "run_start"):]
        arm = recs[0]["policy"]
        if arm not in ARMS:
            continue
        scores, last = {}, None
        for r in recs:
            if "per_entity" in r and r.get("source_hash"):
                scores[r["source_hash"]] = r["per_entity"]
            if r["kind"] == "probe":
                fails = _failing_names(scores.get(r.get("best_hash")))
                expr = r["expression"]
                probes[ARMS[arm][0]].append(dict(
                    script=recs[0]["script"], arm=arm, expr=expr, result=r["result"],
                    error=r["result"].lstrip().startswith(("Error", "ERROR")),
                    known=bool(fails) if r.get("best_hash") in scores else None,
                    targets=any(re.search(rf"(?<![\w.]){re.escape(n)}(?![\w])", expr) for n in fails)))
    routes = collections.defaultdict(collections.Counter)
    for f in sorted((out_dir / "trajectories").glob("*.jsonl")):
        recs = [json.loads(l) for l in f.open(encoding="utf-8")]
        recs = recs[max(i for i, r in enumerate(recs) if r["kind"] == "run_start"):]
        for r in recs:
            if r["kind"] == "route" and r["prober_action"] in ("rewrite", "replace_entity"):
                routes[recs[0]["policy"]]["declined (prober's rewrite used)" if "rewriter_declined" in r else
                                          "after the nudge" if len(r.get("rewriter_tries", [])) > 1 else
                                          "first ask"] += 1
    print("\nrewrite turns, written by the rewriter:")
    for arm in ARMS:
        print(f"  {arm:10s} {dict(routes[arm])}")
    chains_by_prober = collections.Counter()
    for (_, arm, _) in rows:
        chains_by_prober[ARMS[arm][0]] += 1
    print("\nprobes, by prober")
    for p, ps in probes.items():
        known = [x for x in ps if x["known"]]
        print(f"  {p:4s} {len(ps):4d} probes ({len(ps) / max(1, chains_by_prober[p]):.2f}/chain)  "
              f"error {sum(x['error'] for x in ps) / len(ps):.0%}  "
              f"names a failing entity {sum(x['targets'] for x in known)}/{len(known)}  "
              f"median result {st.median(len(x['result']) for x in ps):.0f} chars")
    rng = random.Random(SEED)
    with (out_dir / "probe_sample.txt").open("w", encoding="utf-8") as f:
        for p, ps in probes.items():
            for i, x in enumerate(rng.sample(ps, min(25, len(ps))), 1):
                f.write(f"\n#### {p} {i} {x['script']} ({x['arm']})\n--- expression\n{x['expr'][:1500]}\n"
                        f"--- result\n{x['result'][:800]}\n")
    print(f"  25 probes per prober to read: {out_dir / 'probe_sample.txt'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "analyze", "chains"])
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--budget", type=float, default=5.0)
    ap.add_argument("--reserve", type=float, default=0.5)
    ap.add_argument("--per-state", type=int, default=None)
    ap.add_argument("--arms", nargs="+", default=list(ARMS))
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    if a.cmd == "run":
        run(a.workers, a.budget, a.reserve, a.per_state, a.arms, Path(a.out), a.limit)
    elif a.cmd == "chains":
        cs = chains(a.per_state)
        print(f"{len(cs)} chains in {len({k[0] for k, _ in cs})} states")
    else:
        analyze(Path(a.out))

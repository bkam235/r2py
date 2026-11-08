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
    "entity_esc_ew3": dict(entity_repair=True, escalate_after=2, entity_width=3),   # three repairs per failing entity
    "beam3": dict(entity_repair=False, escalate_after=None, width=3, beam=dict(rounds=3, steps=4)),   # restart from the best states
    "rewrite_rt": dict(entity_repair=False, escalate_after=None, runtime=str(ROOT / "work/runtime/pilot")),   # verified R functions offered
    "rewrite_loc": dict(entity_repair=False, escalate_after=None, locate=True),     # the harness locates the first diverging call
    "rewrite_w3": dict(entity_repair=False, escalate_after=None, width=3),   # three independent loops, best wins
    # Step 3 of the S1 refinement (2026-10-15): the same agent with a short system prompt (scripts/sysprompt_variants.py).
    "rewrite_w3_S1": dict(entity_repair=False, escalate_after=None, width=3, system="S1"),
    "rewrite_w3_S1b": dict(entity_repair=False, escalate_after=None, width=3, system="S1b"),
    # Guided step and crash fallback (registered 2026-10-16), against rewrite_w3 (crash_first "off" by default).
    "rewrite_w3_crashfb": dict(entity_repair=False, escalate_after=None, width=3, crash_first="fallback"),
    "guided_w1k3": dict(entity_repair=False, escalate_after=None, width=1, guided_k=3),   # ~ the calls of width 3
    "guided_w1k3s": dict(entity_repair=False, escalate_after=None, width=1, guided_k=3, guided_mode="struct"),
    # 3 per step (registered 2026-10-17): one chain, 3 unguided rewrites per step, the best that passes review kept.
    "rewrite_w1k3": dict(entity_repair=False, escalate_after=None, width=1, guided_k=3, guided_mode="off"),
    # Patience continuation (registered 2026-10-18): two more steps from a chain that stalled while crashing.
    "continue2": dict(entity_repair=False, escalate_after=None, width=1, max_steps=2),
    # Plateau continuations (registered 2026-10-18): three more steps from a running run's final program.
    # New default for crashing starts (2026-10-18): width 6 and patience 5 while the program crashes.
    "rewrite_w3_crash6p5": dict(entity_repair=False, escalate_after=None, width=3, crash_width=6, crash_stalls=5),
    # The production default as of 2026-10-20: the above plus conversation mode from step 2 on.
    "default_2026_10_20": dict(entity_repair=False, escalate_after=None, width=3, crash_width=6, crash_stalls=5,
                               converse=True),
    # The production default as of 2026-11-01: the above plus entity-addressed feedback.
    "default_2026_11_01": dict(entity_repair=False, escalate_after=None, width=3, crash_width=6, crash_stalls=5,
                               converse=True, entity_feedback=True),
    # Test refuse-done (registered 2026-11-06): the default, and below the threshold "done" counts as a failed step.
    # Capability ceiling (2026-11-08): the default with the translating agent on GLM 5.3 (Novita fp8, the person's
    # choice); review, audit and mapping stay on the manifest's model. Descriptive, not a candidate default.
    "default_2026_11_01_glm53": dict(entity_repair=False, escalate_after=None, width=3, crash_width=6, crash_stalls=5,
                                     converse=True, entity_feedback=True, agent_model="openrouter:z-ai/glm-5.3",
                                     agent_provider={"only": ["novita/fp8"], "allow_fallbacks": False}),
    # The same with GLM's reasoning capped at 8k tokens and the agent's output limit at 36k (2026-11-08: uncapped,
    # its first answers spent all 16,384 tokens on reasoning and returned no code).
    "default_2026_11_01_glm53_r8k": dict(entity_repair=False, escalate_after=None, width=3, crash_width=6,
                                         crash_stalls=5, converse=True, entity_feedback=True,
                                         agent_model="openrouter:z-ai/glm-5.3",
                                         agent_provider={"only": ["novita/fp8"], "allow_fallbacks": False},
                                         agent_reasoning={"max_tokens": 8000}, agent_max_tokens=36000),
    # Free probes (2026-11-08): a probe_r costs no stall and shows its result (2,000 characters); the default, and the
    # GLM ceiling policy, otherwise unchanged.
    "default_2026_11_01_fp": dict(entity_repair=False, escalate_after=None, width=3, crash_width=6, crash_stalls=5,
                                  converse=True, entity_feedback=True, free_probe=True),
    "default_2026_11_01_glm53_r8k_fp": dict(entity_repair=False, escalate_after=None, width=3, crash_width=6,
                                            crash_stalls=5, converse=True, entity_feedback=True,
                                            agent_model="openrouter:z-ai/glm-5.3",
                                            agent_provider={"only": ["novita/fp8"], "allow_fallbacks": False},
                                            agent_reasoning={"max_tokens": 8000}, agent_max_tokens=36000,
                                            free_probe=True),
    # Test free-probe-stall2 (2026-11-08): saved chains continued at their stall-2 point (scripts/stall2_continue.py),
    # with the default hint, and with free probes and the probe hint.
    "stall2_default": dict(entity_repair=False, escalate_after=None, width=1, converse=True, entity_feedback=True,
                           start_stalls=2, max_steps=8),
    "stall2_fp": dict(entity_repair=False, escalate_after=None, width=1, converse=True, entity_feedback=True,
                      start_stalls=2, max_steps=8, free_probe=True),
    # Test model-screen-stall2 (2026-11-08): the same continuations with free probes evaluated in the script's state
    # (probe_state), the agent on Gemma or on a cheap model (pinned provider, reasoning capped as for GLM 5.3); the
    # review stays on Gemma.
    "stall2_ps": dict(entity_repair=False, escalate_after=None, width=1, converse=True, entity_feedback=True,
                      start_stalls=2, max_steps=8, free_probe=True, probe_state=True),
    **{f"stall2_ps_{tag}": dict(entity_repair=False, escalate_after=None, width=1, converse=True, entity_feedback=True,
                                start_stalls=2, max_steps=8, free_probe=True, probe_state=True,
                                agent_model=f"openrouter:{model}",
                                agent_provider={"only": [provider], "allow_fallbacks": False},
                                agent_reasoning={"max_tokens": 8000}, agent_max_tokens=36000)
       for tag, model, provider in (("glmflash", "z-ai/glm-5.3-flash", "novita/fp8"),
                                    ("qwenflash", "qwen/qwen3.7-flash", "alibaba"),
                                    ("gptoss", "openai/gpt-oss-120b", "deepinfra/bf16"),
                                    ("dsflash", "deepseek/deepseek-v4.1-flash-1017", "deepinfra/fp8"))},
    "default_2026_11_01_rd": dict(entity_repair=False, escalate_after=None, width=3, crash_width=6, crash_stalls=5,
                                  converse=True, entity_feedback=True, refuse_done=True),
    "continue3": dict(entity_repair=False, escalate_after=None, width=1, max_steps=3),
    "continue3_eq": dict(entity_repair=False, escalate_after=None, width=1, max_steps=3, accept_equal=True),
    # Upper bound on retrieval: a library holding a verified example of exactly the functions this
    # script calls, built by scripts/oracle_library.py (perfect coverage, perfect retrieval).
    "rewrite_w3_oracle": dict(entity_repair=False, escalate_after=None, width=3, oracle=True),
    # Intra-script runtime: before the agent starts, verify the R functions the frozen state fails on
    # (r2py/runtime/ondemand.py), in a private copy of the starting store (--runtime-dir, default empty)
    # so that no run can hand a verified function to another.
    "rewrite_w3_ondemand": dict(entity_repair=False, escalate_after=None, width=3,
                                ondemand=dict(max_functions=2, budget_s=900, rounds=2, attempts=4)),
    # The same agent with a fixed store and no on-demand step: the inter-script arm (--runtime-dir).
    "rewrite_w3_store": dict(entity_repair=False, escalate_after=None, width=3, runtime="from --runtime-dir"),
}


POOL_RUNNING, POOL_CRASHING = 40, 20     # training pool (2026-10-16): states below 0.9, both strata
TRAIN_SOURCES = ROOT / "work/heldout/train_outputs"
TRAIN_MAPS = ROOT / "work/reverify/script_maps"


def training_states(max_start: float = 0.9, seed: int = 0) -> dict[str, dict]:
    """A fixed pool of training translations to replay: 40 that run and 20 that crash, all below ``max_start``.

    The 20 dev states give intervals of about +-0.06 per arm comparison, wider than the effects now being tested
    (S1 +0.017, locator +0.029, crash-first -0.019). The training translations add 223 states that run and 26 that
    crash, re-verified offline (work/reverify/rows_v3.jsonl); half of the dev states' noise is crash-or-not, so the
    pool keeps a crashing stratum to be reported apart.
    """
    import random
    from r2py.harness import trajectory
    rows = [json.loads(l) for l in (ROOT / "work/reverify/rows_v3.jsonl").open(encoding="utf-8")]
    rows = [r for r in rows if "error" not in r and r["aggregate"] < max_start
            and (TRAIN_SOURCES / f"{Path(r['script']).stem}.py").exists()
            and (TRAIN_MAPS / f"{Path(r['script']).stem}.pkl").exists()]
    rng = random.Random(seed)
    running = sorted(r["script"] for r in rows if r.get("py_exit") == 0)
    crashing = sorted(r["script"] for r in rows if r.get("py_exit") != 0)
    picked = rng.sample(running, min(POOL_RUNNING, len(running))) + rng.sample(crashing, min(POOL_CRASHING, len(crashing)))
    by = {r["script"]: r for r in rows}
    out = {}
    for name in sorted(picked):
        src = (TRAIN_SOURCES / f"{Path(name).stem}.py").read_text(encoding="utf-8")
        out[name] = {"source": src, "label": "training", "aggregate": by[name]["aggregate"],
                     "hash": trajectory.source_hash(src)}
    return out


def heldout_states() -> dict[str, dict]:
    """The meta-loop's held-out pool (experiments/pools/heldout.json, frozen 2026-10-24 by select_heldout.py): 46
    training translations outside the training pool, for confirming a change before it becomes the default."""
    from r2py.harness import trajectory
    names = json.loads((ROOT / "experiments/pools/heldout.json").read_text(encoding="utf-8"))["states"]
    by = {json.loads(l)["script"]: json.loads(l) for l in (ROOT / "work/reverify/rows_v3.jsonl").open(encoding="utf-8")}
    out = {}
    for name in names:
        src = (TRAIN_SOURCES / f"{Path(name).stem}.py").read_text(encoding="utf-8")
        out[name] = {"source": src, "label": "heldout", "aggregate": by[name]["aggregate"],
                     "hash": trajectory.source_hash(src)}
    return out


def pool_states(pool: str, max_start: float = 0.9) -> dict[str, dict]:
    """`training` (where changes are tried) or `heldout` (where winners are confirmed)."""
    return heldout_states() if pool == "heldout" else training_states(max_start)


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
    from r2py.harness.beam import reason_beam
    from r2py.harness.audit import format_audit_for_agent, static_audit
    from r2py.harness.tools import HarnessTools
    from r2py.library import PatternLibrary
    from r2py.stage1.runner import strip_r_guards

    manifest = ho.load_manifest(task["manifest"])
    cfg = manifest["protocol"]["translate"]
    row = {k: task[k] for k in ("script", "policy", "sample", "label", "start_hash")}
    from r2py.scoring import scoring_version
    row["scoring_version"] = scoring_version()   # scores compare only within one scoring epoch
    started = time.monotonic()
    out_dir = Path(task["out_dir"])
    # agent_model (2026-11-08): the translating agent on another model, pinned to agent_provider; the review gate,
    # the static audit and the entity mapping stay on the manifest's model, so only the translator changes.
    agent_model = POLICIES[task["policy"]].get("agent_model")
    settings = ho.llm_settings(manifest)
    if agent_model:
        row["agent_model"] = agent_model
        name = agent_model.removeprefix("openrouter:")
        settings = {**settings, "provider_by_model": {name: POLICIES[task["policy"]]["agent_provider"]}}
        if POLICIES[task["policy"]].get("agent_reasoning"):
            settings["extra_by_model"] = {name: {"reasoning": POLICIES[task["policy"]]["agent_reasoning"]}}
    ho.drain_usage()
    try:
        with ho.pinned_llm(cfg["model"], settings):
            sm = _script_map(task["script"], manifest, Path(task["cache"]))
            with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
                policy = dict(POLICIES[task["policy"]])
                policy.pop("agent_model", None)
                policy.pop("agent_provider", None)
                policy.pop("agent_reasoning", None)
                if "agent_max_tokens" in policy:
                    policy["max_tokens"] = policy.pop("agent_max_tokens")
                runtime_dir = policy.pop("runtime", None)
                lib_dir = Path(task["library"])
                if policy.pop("oracle", False):
                    lib_dir = ROOT / "work/oracle/libs" / Path(task["script"]).stem
                shutil.copytree(lib_dir, Path(tmp) / "lib")
                lib = PatternLibrary(Path(tmp) / "lib")
                row["lib_patterns"] = len(list((Path(tmp) / "lib" / "patterns").glob("*.md")))
                store = None
                ondemand = policy.pop("ondemand", None)
                if runtime_dir == "from --runtime-dir":
                    runtime_dir = task.get("runtime_dir") or None
                if runtime_dir or ondemand:
                    from r2py.runtime.store import RuntimeStore
                    private = Path(tmp) / "runtime"
                    start_store = task.get("runtime_dir") if ondemand else runtime_dir
                    if start_store and Path(start_store).is_dir():
                        shutil.copytree(start_store, private)
                    private.mkdir(exist_ok=True)
                    store = RuntimeStore(private)
                    row["store_start"] = len(store)

                def new_harness():
                    return HarnessTools(sm, lib, model=cfg["model"], data_compare=cfg["data_compare"],
                                        timeout_s=cfg["timeout_s"],
                                        sidecar_filename=f"{Path(task['script']).stem}.r2py_data.json", runtime=store)
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
                if ondemand and store is not None:
                    from r2py.runtime.ondemand import verify_needed
                    recs = verify_needed(sm, start_report, store, model=cfg["model"], **ondemand)
                    row["ondemand"] = recs
                    row["store_after_ondemand"] = len(store)
                    trajectory.log("ondemand", records=recs)
                drain_agent_stats()
                from r2py.harness.tools import drain_cache_stats
                drain_cache_stats()
                system = policy.pop("system", None)
                if system:
                    sys.path.insert(0, str(ROOT / "scripts"))
                    from sysprompt_variants import loop_variants
                    policy["system_override"] = loop_variants()[system]
                width = policy.pop("width", 1)
                crash_width = policy.pop("crash_width", None)
                if crash_width and start_report.py_exit_code != 0:
                    width = crash_width
                    from r2py.loop import DEFAULT_CRASH_BUDGET_FACTOR
                    task = {**task, "budget_s": task["budget_s"] * DEFAULT_CRASH_BUDGET_FACTOR}   # as run_loop does
                max_steps = policy.pop("max_steps", cfg["max_iters"])   # continuation tests stop early (2026-10-18)
                beam_cfg = policy.pop("beam", None)
                harnesses = [harness] + [new_harness() for _ in range(width - 1)]
                if agent_model:
                    policy["review_model"] = cfg["model"]
                common = dict(current_source=task["source"], score_report=start_report, script_map=sm,
                              model=agent_model or cfg["model"],
                              score_threshold=cfg["score_threshold"], max_stalls=cfg["max_stalls"],
                              budget_s=task["budget_s"], audit_feedback=audit, replace_entity=False, **policy)
                if beam_cfg:
                    result = reason_beam(harnesses, max_steps=beam_cfg["steps"], max_rounds=beam_cfg["rounds"], **common)
                else:
                    result = reason_wide(harnesses, max_steps=max_steps, **common)
                final = result[1].aggregate if result else start_report.aggregate
                row.update(final_score=round(final, 4), improved=bool(result and final > start_report.aggregate + 1e-9),
                           final_exit=(result[1].py_exit_code if result else start_report.py_exit_code))
                row["agent"] = drain_agent_stats()
                row["llm_steps"] = sum(row["agent"]["action"].values())   # the cost measure: model calls per run
                # how each verification attributed entities: sentinels, deterministic restoration, or a model mapping
                # (the one remaining source of scoring noise, 2026-10-17)
                row["verify_paths"] = drain_cache_stats()
                trajectory.end(final_score=row["final_score"])
    except Exception as exc:
        row["error"] = f"{type(exc).__name__}: {exc}"[:300]
    row["usage"] = ho.drain_usage()   # tokens and cost per model of this run (2026-11-08)
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
    ap.add_argument("--arms", nargs="+", default=[], help="dev arms whose best seeds are the frozen states")
    ap.add_argument("--pool", choices=["dev", "training", "heldout"], default="dev",
                    help="training: a fixed pool of 40 running + 20 crashing training translations; "
                         "heldout: the 46 states for confirming winners (experiments/pools/heldout.json)")
    ap.add_argument("--policies", nargs="+", default=["rewrite", "entity_esc"], choices=sorted(POLICIES))
    ap.add_argument("--samples", type=int, default=3)
    ap.add_argument("--workers", type=int, default=6)
    from expkit import add_guard_args
    add_guard_args(ap)
    ap.add_argument("--max-start", type=float, default=0.9, help="skip states whose seed already reaches this")
    ap.add_argument("--only", nargs="+", help="substrings of script names")
    ap.add_argument("--budget-s", type=float, default=1200)
    ap.add_argument("--manifest", default=str(ROOT / "experiments/dev_run/manifest.json"))
    ap.add_argument("--library", default=str(ROOT / "work/dev_run/checkpoints/empty"))
    ap.add_argument("--runtime-dir", default=None,
                    help="starting runtime store for rewrite_w3_store / rewrite_w3_ondemand (copied per run)")
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

    if args.pool in ("training", "heldout"):
        states = pool_states(args.pool, args.max_start)
        cache = str(TRAIN_MAPS)   # analysed maps are cached; the loop keeps the dev manifest's settings (max_stalls 3)
    else:
        states = best_states(args.arms, args.max_start)
        cache = str(ROOT / "work/replay/script_maps")
    if args.only:
        states = {n: s for n, s in states.items() if any(o in n for o in args.only)}
    finished = {(r["script"], r["policy"], r["sample"]) for r in done if "final_score" in r and not r.get("invalid")}
    tasks = []
    # sample-major order: every state/policy gets sample 0 before any gets sample 1, so an early stop
    # still leaves a balanced design
    for sample in range(args.samples):
        for name, s in sorted(states.items()):
            for policy in args.policies:
                if (name, policy, sample) in finished:
                    continue
                tasks.append(dict(script=name, policy=policy, sample=sample, source=s["source"], label=s["label"],
                                  start_hash=s["hash"], manifest=args.manifest, library=args.library, runtime_dir=args.runtime_dir,
                                  cache=cache, out_dir=str(out.parent),
                                  budget_s=args.budget_s))
    listing = ", ".join("%s(%.2f)" % (n[:18], s["aggregate"]) for n, s in sorted(states.items()))
    print(f"{len(states)} frozen states: {listing}")
    print(f"{len(tasks)} runs to do ({len(finished)} already finished), {args.workers} workers", flush=True)

    ctx = multiprocessing.get_context("spawn")
    from expkit import RunGuard
    with RunGuard(out.parent, budget=args.budget, reserve=args.reserve) as guard, \
            ctx.Pool(args.workers) as pool, out.open("a", encoding="utf-8") as f:
        for i, row in enumerate(pool.imap_unordered(run_one, tasks), 1):
            row = guard.annotate(row)
            f.write(json.dumps(row) + "\n")
            f.flush()
            done.append(row)
            print(f"[{i}/{len(tasks)}] {row['script'][:36]:36s} {row['policy']:11s} s{row['sample']}: "
                  + (f"{row['start_score']:.2f} -> {row['final_score']:.2f} ({row['seconds'] / 60:.0f} min)"
                     if "final_score" in row else f"ERROR {row.get('error', '')[:80]}"), flush=True)
            if guard.should_stop():   # budget or reserve reached: stop cleanly; the same command resumes
                print(f"[guard] stopping: {guard.stop_reason}", flush=True)
                pool.terminate()
                break
    print("\n" + summarise(done))
    from health_report import report
    try:   # a failing report must not hide the run's results, which are already written
        (out.parent / "health_report.md").write_text(report(out.parent.resolve()), encoding="utf-8")
        print(f"health report: {out.parent / 'health_report.md'}")
    except Exception as e:
        print(f"health report failed: {type(e).__name__}: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

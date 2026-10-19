"""Step-level A/B: what does ONE agent step do from a frozen state, with and without guidance? (registered 2026-10-16)

Full-loop replays take hours per answer and their outcome is dominated by crash-or-not. A mechanism that helps
must raise what one step does, so this measures one step directly: the production turn and system prompt, one
model call, the loop's gates (data shim, argument order, syntax, imports; the hardcoding review when the
candidate improves, as in the loop), then verification.

    python scripts/step_ab.py guidable            # step 1: offline, no model calls; freezes the guidance
    python scripts/step_ab.py run --samples 4     # step 2
    python scripts/step_ab.py summary

Arms: U (no guidance), GV (whole-value guidance: R's print, or R's values <= 1,500 characters), GS (structured:
the verifier's per-path differences, the first differing printed lines, the locator's first diverging call).
"""
from __future__ import annotations

import argparse
import json
import multiprocessing
import pickle
import random
import statistics as st
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

OUT = ROOT / "work" / "step_ab"
ARMS = ("U", "GV", "GS")
GEMMA = "openrouter:google/gemma-4-31b-it"


def _tools(sm, stem):
    from prompt_load import _tools as t
    return t(sm, stem)


def running_states() -> dict[str, dict]:
    import replay
    rows = {json.loads(l)["script"]: json.loads(l) for l in (ROOT / "work/reverify/rows_v3.jsonl").open(encoding="utf-8")}
    return {n: s for n, s in replay.training_states().items() if rows[n].get("py_exit") == 0}


def _setup(name: str, state: dict):
    from r2py.stage2.sentinel_mapper import ranges_from_sentinels
    stem = Path(name).stem
    sm = pickle.loads((ROOT / "work/reverify/script_maps" / f"{stem}.pkl").read_bytes())
    tools = _tools(sm, stem)
    tools.note_reference(state["source"])
    rep = tools.verify(state["source"])
    annotated = tools.last_annotated_source or state["source"]
    assert ranges_from_sentinels(annotated) is not None
    return stem, sm, tools, rep, annotated


def guidable() -> None:
    """Step 1: per running state, the guidance each arm would get and the loss it could reach (no model calls)."""
    from r2py.harness.agent import _guided_target, _guided_target_structured
    from r2py.harness.objective import entity_score
    OUT.mkdir(parents=True, exist_ok=True)
    targets = {}
    for name, state in sorted(running_states().items()):
        try:
            stem, sm, tools, rep, annotated = _setup(name, state)
        except Exception as exc:
            print(f"   {name[:46]:<48}setup failed: {exc}"[:140], flush=True)
            continue
        if rep.py_exit_code != 0:
            print(f"   {name[:46]:<48}start no longer runs, skipped", flush=True)
            continue
        loss = {e: 1 - entity_score(es) for e, es in rep.by_entity.items() if es.active_dims}
        gv = _guided_target(rep, sm, {})
        gs = _guided_target_structured(rep, sm, {}, tools, annotated)
        targets[name] = {"aggregate": rep.aggregate, "loss": round(sum(loss.values()), 3),
                         "GV": gv, "GS": gs,
                         "GV_loss": round(loss.get(gv[0], 0), 3) if gv else 0.0,
                         "GS_loss": round(loss.get(gs[0], 0), 3) if gs else 0.0}
        print(f"   {name[:46]:<48}GV {gv[0] if gv else '-':<18} GS {gs[0] if gs else '-':<18}", flush=True)
    (OUT / "targets.json").write_text(json.dumps(targets, indent=1), encoding="utf-8")
    n = len(targets)
    tot = sum(t["loss"] for t in targets.values()) or 1
    lines = [f"{n} running states verified",
             f"GV (whole value): target in {sum(bool(t['GV']) for t in targets.values())} states, "
             f"{sum(t['GV_loss'] for t in targets.values()) / tot:.0%} of their loss in the targeted entity",
             f"GS (structured):  target in {sum(bool(t['GS']) for t in targets.values())} states, "
             f"{sum(t['GS_loss'] for t in targets.values()) / tot:.0%} of their loss in the targeted entity",
             f"GS with a locator note: {sum(bool(t['GS']) and 'first' in t['GS'][1] for t in targets.values())}"]
    text = "\n".join(lines)
    (OUT / "guidable.txt").write_text(text + "\n", encoding="utf-8")
    print("\n" + text)


def run_one(task: dict) -> dict:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    from r2py import heldout as ho
    from r2py.harness import objective as obj
    from r2py.harness import prompt as P
    from r2py.harness.agent import _check_syntax, _parse_action, restore_data_shim
    from r2py.harness.review import review_translation
    from r2py.stage0.env.module_check import unavailable_imports
    from r2py.stage0.sandbox.py_sandbox import _SKIP_PACKAGES
    from r2py.stage2 import llm
    from r2py.stage2.argorder import repair_argument_order
    from r2py.stage2.stitch import hide_data_shim, show_data_shim

    name, arm, t = task["name"], task["arm"], task["targets"]
    row = {"script": name, "arm": arm, "sample": task["sample"]}
    started = time.monotonic()
    try:
        manifest = ho.load_manifest(ROOT / "experiments/dev_run/manifest.json")
        cfg = manifest["protocol"]["translate"]
        stem, sm, tools, base, annotated = _setup(name, task["state"])
        row["before"] = round(base.aggregate, 4)
        row["exit_before"] = base.py_exit_code
        guide = t.get(arm) if arm in ("GV", "GS") else None
        row["guided_entity"] = guide[0] if guide else None
        common = (t.get("GS") or t.get("GV") or [None])[0]       # the same entity is followed in every arm
        row["common_entity"] = common
        if common:
            row["common_before"] = round(obj.entity_score(base.by_entity[common]), 4)
        msgs = P.build_agent_turn(sm.source or "", hide_data_shim(annotated), base, sm, 1, cfg["max_iters"], 10,
                                  history=[], sidecar_filename=f"{stem}.r2py_data.json")
        if guide:
            msgs[-1]["content"] += "\n\n" + guide[1]
        if arm in ("S", "N"):   # feedback ablation (2026-10-19)
            msgs[-1]["content"] = _ablate_feedback(msgs[-1]["content"], arm)
        from r2py.harness.manual import enforce_interfaces, interface_note
        if arm == "F":      # manual stage 1: the best program's helper interfaces are frozen for this step
            note = interface_note(annotated)
            if note:
                msgs[-1]["content"] += "\n\n" + note
            row["frozen_helpers"] = bool(note)
        system =P.without_replace_entity(P.with_runtime_note(P.AGENT_SYSTEM_PROMPT_OPENROUTER))
        with ho.pinned_llm(GEMMA, ho.llm_settings(manifest)):
            raw = llm.call(msgs, system, model=GEMMA, max_tokens=16384)
            action = _parse_action(raw)
            if not action or action.get("action") != "rewrite" or not action.get("new_source"):
                row.update(outcome="no rewrite", gain=0.0, improved=False)
                return row
            src = show_data_shim(annotated, action["new_source"])
            src, _ = restore_data_shim(annotated, src)
            enforced, info = enforce_interfaces(annotated, src)
            row["interface_changed"] = info["changed"]            # attempted, measured in every arm
            if arm == "F":
                src = enforced
                row["interface_restored"] = info["restored"]
            src, _ = repair_argument_order(src)
            code_dir = Path(task["out"]) / "code"
            code_dir.mkdir(parents=True, exist_ok=True)
            (code_dir / f"{stem}.{arm}.{task['sample']}.all.py").write_text(src, encoding="utf-8")
            if _check_syntax(src) or unavailable_imports(src, _SKIP_PACKAGES):
                row.update(outcome="gate rejected", gain=0.0, improved=False)
                return row
            new = tools.verify(src)
            from paste_check import check as paste_check
            row["paste"] = paste_check(src, annotated, sm.source or "", getattr(sm, "entity_bundles", {}) or {})
            row["after"] = round(new.aggregate, 4)
            row["exit_after"] = new.py_exit_code
            if common and common in new.by_entity:
                row["common_after"] = round(obj.entity_score(new.by_entity[common]), 4)
            # damage: entities verified in the best state (>= 0.95) that this candidate pushes below 0.95
            row["verified_before"] = sum(obj.entity_score(es) >= 0.95 for es in base.by_entity.values())
            row["damaged"] = sum(1 for k, es in base.by_entity.items() if obj.entity_score(es) >= 0.95
                                 and (k not in new.by_entity or obj.entity_score(new.by_entity[k]) < 0.95))
            better = obj.better(new, base)
            if better and new.py_exit_code == 0:   # as in the loop: the review judges what runs
                passed, reason = review_translation(sm.source or "", src, sm, model=GEMMA)
                row["review_rejected"] = not passed
                row["review_reason"] = (reason or "")[:600]
                # keep every improving candidate for the manual check of the review (2026-10-16)
                code_dir = Path(task["out"]) / "code"
                code_dir.mkdir(parents=True, exist_ok=True)
                (code_dir / f"{stem}.{arm}.{task['sample']}.py").write_text(src, encoding="utf-8")
                if not (code_dir / f"{stem}.before.py").exists():
                    (code_dir / f"{stem}.before.py").write_text(annotated, encoding="utf-8")
                better = passed
        row["improved"] = bool(better)
        row["gain"] = round(max(0.0, new.aggregate - base.aggregate), 4) if better else 0.0
        row["outcome"] = "verified"
    except Exception as exc:
        from r2py.stage2 import llm as _l
        kind = _l.classify_failure(exc)
        row["outcome"] = "provider_unavailable" if kind in ("credits", "rate_limit", "network", "server") \
            else f"error: {type(exc).__name__}: {exc}"[:200]
    row["seconds"] = round(time.monotonic() - started, 1)
    return row


def _ablate_feedback(content: str, arm: str) -> str:
    """The turn with its verification section cut to the scores (S) or removed (N); everything else unchanged."""
    head = "### Verification result\n"
    i = content.index(head)
    j = content.index("\n### ", i + len(head))
    if arm == "N":
        return content[:i] + content[j + 1:]
    section = content[i + len(head):j]
    cuts = [k for k in (section.find("\n\nOutput comparisons"), section.find("\n\nVerifier feedback")) if k >= 0]
    return content[:i + len(head)] + section[:min(cuts) if cuts else len(section)] + "\n" + content[j:]


def run(samples: int, workers: int, arms=ARMS, with_crashing: bool = False) -> None:
    targets = json.loads((ROOT / "work/step_ab/targets.json").read_text(encoding="utf-8"))
    import replay
    states = replay.training_states() if with_crashing else running_states()
    targets = {n: targets.get(n, {}) for n in states}
    path = OUT / "results.jsonl"
    done = [json.loads(l) for l in path.open(encoding="utf-8")] if path.exists() else []
    finished = {(r["script"], r["arm"], r["sample"]) for r in done if r.get("outcome") != "provider_unavailable"}
    tasks = [{"name": n, "arm": a, "sample": s, "state": states[n], "targets": targets[n], "out": str(OUT)}
             for s in range(samples) for n in sorted(targets) for a in arms if (n, a, s) not in finished]
    print(f"{len(targets)} states x {len(arms)} arms x {samples} samples: {len(tasks)} steps to do", flush=True)
    outages = 0
    with multiprocessing.get_context("spawn").Pool(workers) as pool, path.open("a", encoding="utf-8") as fh:
        for i, row in enumerate(pool.imap_unordered(run_one, tasks), 1):
            fh.write(json.dumps(row) + "\n")
            fh.flush()
            outages += row.get("outcome") == "provider_unavailable"
            print(f"[{i}/{len(tasks)}] {row['script'][:36]:<38}{row['arm']:<3}s{row['sample']} "
                  f"{row.get('outcome', '')[:20]:<20} {row.get('before')}->{row.get('after')} gain {row.get('gain')}",
                  flush=True)
            if outages >= 3:
                print("3 provider outages: stopping; the same command resumes", flush=True)
                pool.terminate()
                break


def summary() -> str:
    rows = [json.loads(l) for l in (OUT / "results.jsonl").open(encoding="utf-8")]
    rows = [r for r in rows if r.get("outcome") != "provider_unavailable"]
    lines = [f"{len(rows)} steps; errors {sum(str(r.get('outcome', '')).startswith('error') for r in rows)}"]
    per = defaultdict(lambda: defaultdict(list))
    for r in rows:
        per[r["arm"]][r["script"]].append(r)
    for arm in ARMS:
        rs = [r for v in per[arm].values() for r in v]
        if not rs:
            continue
        ce = [r["common_after"] - r["common_before"] for r in rs if "common_after" in r]
        p = st.mean(r.get("improved", False) for r in rs)
        lines.append(f"{arm:<3} steps {len(rs):>4}  P(improve) {p:.2f}  (best of 3: {1 - (1 - p) ** 3:.2f})  "
                     f"mean realized gain {st.mean(r.get('gain', 0) for r in rs):+.4f}  "
                     f"followed entity {st.mean(ce) if ce else 0:+.3f}  "
                     f"no rewrite {sum(r.get('outcome') == 'no rewrite' for r in rs)}  "
                     f"gate {sum(r.get('outcome') == 'gate rejected' for r in rs)}  "
                     f"review rej {sum(bool(r.get('review_rejected')) for r in rs)}")
    rng = random.Random(0)
    winner = None
    for arm in ("GV", "GS"):
        ks = sorted(set(per[arm]) & set(per["U"]))
        for metric, f in (("realized gain", lambda r: r.get("gain", 0)),
                          ("P(improve)", lambda r: float(r.get("improved", False)))):
            diff = [st.mean(map(f, per[arm][k])) - st.mean(map(f, per["U"][k])) for k in ks]
            boots = sorted(st.mean(rng.choice(diff) for _ in diff) for _ in range(5000))
            lines.append(f"{arm} vs U, {metric}: {st.mean(diff):+.4f} [{boots[125]:+.4f}, {boots[4874]:+.4f}]  "
                         f"({len(ks)} states)")
            if metric == "realized gain" and boots[125] > 0 and (winner is None or st.mean(diff) > winner[1]):
                winner = (arm, st.mean(diff))
    lines.append(f"\nDecision: {('winner ' + winner[0]) if winner else 'no guided arm beats U'}")
    return "\n".join(lines)


def main() -> int:
    from r2py.keepawake import keep_awake
    keep_awake()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("guidable")
    p = sub.add_parser("run")
    p.add_argument("--samples", type=int, default=4)
    p.add_argument("--workers", type=int, default=6)
    p.add_argument("--arms", nargs="+", default=list(ARMS), choices=["U", "GV", "GS", "F", "S", "N"])
    p.add_argument("--with-crashing", action="store_true", help="the whole training pool, crashing starts included")
    sp = sub.add_parser("summary")
    for q in (p, sp):
        q.add_argument("--tag", default="", help="separate output directory; guidance stays work/step_ab/targets.json")
    args = ap.parse_args()
    global OUT
    if getattr(args, "tag", ""):
        OUT = OUT.with_name(f"step_ab_{args.tag}")
        OUT.mkdir(parents=True, exist_ok=True)
    if args.cmd == "guidable":
        guidable()
        return 0
    if args.cmd == "run":
        run(args.samples, args.workers, args.arms, args.with_crashing)
    text = summary()
    print("\n" + text)
    (OUT / "summary.txt").write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""How must guidance be presented for the model to act on it? One model call per arm.

Everything measured so far says the model ignores knowledge offered as a prompt example: imitation
sits at chance even when the example is of the entity's own function and the two R statements are
related (`scripts/imitation_probe.py`). That could be the presentation (buried 69% into an 8.8k-character
prompt, introduced by a soft "use ... to inform your rewrite") or the model. This rig separates the two
by holding the *content* fixed at the strongest possible value -- the correct Python for that very entity,
taken from a run that scored it 1.0 -- and varying only how it is put in front of the model:

  none            no guidance at all (control: what the model does unaided)
  library         in the pattern-library section, where the library puts it today
  last_imperative at the very end of the prompt, naming the entity, as an instruction
  entity_only     the same, plus a demand to answer with replace_entity for that entity alone

Each case is one frozen state, one failing entity, one model call, then the action is applied and
verified. Reported per arm: how much of the guidance appears in the entity's new code (adoption) and
what the entity's score does. If no presentation beats `none`, presentation is not the lever.

    python scripts/prompt_arms.py --samples 1 --workers 6
    python scripts/prompt_arms.py --summary-only
"""
from __future__ import annotations

import argparse
import contextlib
import json
import multiprocessing
import pickle
import re
import statistics as st
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

ARMS_DIRS = [f"work/smoke/{a}" for a in ("20261001_112951", "20261001_140509", "20261001_165951")]
MAPS = ROOT / "work" / "replay" / "script_maps"
OUT = ROOT / "work" / "prompt_arms" / "results.jsonl"
TREATMENTS = ("none", "library", "last_imperative", "entity_only")
GEMMA = "openrouter:google/gemma-4-31b-it"
HAIKU = "claude-haiku-4-5"          # a control for the model factor, not a candidate translator
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def guidance_text(eid: str, code: str, imperative: bool) -> str:
    if not imperative:
        return code
    return ("### Verified translation for this statement\n"
            f"The following Python is a verified, execution-equivalent translation of entity "
            f"`{eid}` of this script. It was checked against R's own output for this exact statement.\n"
            "```python\n" + code + "\n```\n"
            f"Use it for `{eid}` as written, adapting only names that must match the surrounding code. "
            "Do not replace it with your own version of that statement.")


def distinctive(code: str, r_text: str) -> set[str]:
    import keyword
    common = set(keyword.kwlist) | {"np", "pd", "self", "print", "len", "str", "int", "float", "list",
                                    "dict", "range", "True", "False", "None", "import", "return"}
    r_tokens = {t.lower() for t in IDENT.findall(r_text)}
    return {t for t in IDENT.findall(code)
            if len(t) > 2 and t not in common and t.lower() not in r_tokens}


def run_one(task: dict) -> dict:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    from r2py import heldout as ho
    from r2py.harness.agent import _parse_action
    from r2py.harness.prompt import AGENT_SYSTEM_PROMPT, build_agent_turn, without_replace_entity
    from r2py.harness.tools import HarnessTools
    from r2py.library import PatternLibrary
    from r2py.library.pattern import Pattern, TranslationExample
    from r2py.stage2 import llm
    from r2py.stage2.sentinel_mapper import ranges_from_sentinels
    from r2py.stage2.stitch import hide_data_shim, show_data_shim, splice_entity

    row = {k: task[k] for k in ("script", "entity", "treatment", "sample", "model")}
    started = time.monotonic()
    calls = [0]
    real = llm.call

    def counted(*a, **k):
        calls[0] += 1
        return real(*a, **k)
    try:
        manifest = ho.load_manifest(ROOT / "experiments/dev_run/manifest.json")
        cfg = manifest["protocol"]["translate"]
        stem, eid, treatment = task["script"], task["entity"], task["treatment"]
        sm = pickle.loads((MAPS / f"{stem}.pkl").read_bytes())
        # The harness side (verification, any attribution fallback) keeps the manifest's model in
        # every arm, so only the agent call differs between models.
        tools = HarnessTools(sm, PatternLibrary(ROOT / "work/dev_run/checkpoints/empty"),
                             model=cfg["model"], data_compare=cfg["data_compare"],
                             timeout_s=cfg["timeout_s"], sidecar_filename=f"{stem}.r2py_data.json")
        source = task["source"]
        tools.note_reference(source)
        agent_model = task["model"]
        pin = (ho.pinned_llm(cfg["model"], ho.llm_settings(manifest))
               if agent_model.startswith("openrouter:") else contextlib.nullcontext())
        with pin:
            llm.call = counted
            base = tools.verify(source)
            row["before"] = round(ho.entity_score(base.by_entity[eid]), 4)
            row["aggregate_before"] = round(base.aggregate, 4)
            row["exit_before"] = base.py_exit_code
            row["ran_before"] = bool(base.by_entity[eid].executed_ok)
            if row["before"] > 0.999:
                row["outcome"] = "already correct"     # nothing to repair: no model call made
                return row

            entity = sm.entities[eid]
            r_text = task["r_snippet"]
            patterns = None
            extra = ""
            if treatment == "library":
                pat = Pattern(id="guidance", package=getattr(entity, "package", "") or "base",
                              confidence="tentative", seed=True,
                              guidance=f"Verified translation of `{eid}`; prefer it over guessing.")
                pat.translation_examples = [TranslationExample(
                    r_hash="", r_snippet=r_text, py_snippet=task["code"], score=1.0, script_id=stem)]
                patterns = {eid: [pat]}
            elif treatment in ("last_imperative", "entity_only"):
                extra = guidance_text(eid, task["code"], True)
                if treatment == "entity_only":
                    extra += ("\n\nAnswer with ACTION: replace_entity for this one entity "
                              f"(ENTITY: {eid}) and nothing else. Do not rewrite the whole file.")

            messages = build_agent_turn(sm.source or "", hide_data_shim(source), base, sm, 1,
                                        cfg["max_iters"], 10, history=[], patterns_by_entity=patterns,
                                        sidecar_filename=f"{stem}.r2py_data.json")
            if extra:
                messages[-1]["content"] += "\n\n" + extra
            system = AGENT_SYSTEM_PROMPT if treatment == "entity_only" else without_replace_entity(AGENT_SYSTEM_PROMPT)
            row["prompt_chars"] = sum(len(m["content"]) for m in messages)
            raw = llm.call(messages, system, model=agent_model, max_tokens=16384)
            action = _parse_action(raw)
            row["action"] = (action or {}).get("action", "(unparsed)")
            new_source = (action or {}).get("new_source")
            if not new_source:
                row["outcome"] = "no code"
                return row
            if row["action"] in ("replace_entity", "entity_repair"):
                spliced, err = splice_entity(source, (action or {}).get("entity", "") or eid, new_source)
                if spliced is None:
                    row["outcome"] = f"splice refused: {err[:80]}"
                    return row
                new_source = spliced
            new_source = show_data_shim(source, new_source)
            rep = tools.verify(new_source)
            after = rep.by_entity.get(eid)
            row["after"] = round(ho.entity_score(after), 4) if after else None
            row["aggregate_after"] = round(rep.aggregate, 4)
            ranges = ranges_from_sentinels(new_source)
            lines = new_source.splitlines()
            got = "\n".join(l for a, b in ranges.get(eid, []) for l in lines[a:b + 1])
            want = distinctive(task["code"], r_text)
            row["adoption"] = round(len(want & set(IDENT.findall(got))) / len(want), 4) if want else None
            # Why does a correctly copied statement still score badly? Record what the run looked
            # like, and keep the source: an entity can only be judged inside its whole program.
            row["exit_after"] = rep.py_exit_code
            row["ran_after"] = bool(after and after.executed_ok)
            row["crash_entities"] = list(rep.crash_entities or [])[:3]
            row["crash_before_entity"] = bool(rep.crash_entities) and eid not in (rep.crash_entities or [])
            row["entity_feedback"] = [f"{fb.effect_class.value}: {fb.message}"[:200]
                                      for fb in rep.feedback if fb.entity_id == eid][:2]
            row["entity_code"] = got[:2000]
            src_dir = OUT.parent / "sources"
            src_dir.mkdir(parents=True, exist_ok=True)
            tag = f"{stem}.{eid}.{treatment}.{agent_model.split('/')[-1]}.{task['sample']}"
            (src_dir / f"{tag}.py").write_text(new_source, encoding="utf-8")
            row["outcome"] = "verified"
    except Exception as exc:
        # A provider outage is not a result: the row is discarded by the caller and the case repeated.
        kind = llm.classify_failure(exc)
        if kind in ("credits", "rate_limit", "network", "server") or "402" in str(exc):
            row["outcome"] = "provider_unavailable"
            row["provider"] = kind
        else:
            row["outcome"] = f"error: {type(exc).__name__}: {exc}"[:200]
    finally:
        llm.call = real
    row["llm_calls"] = calls[0]
    row["seconds"] = round(time.monotonic() - started, 1)
    return row


def usable_guidance(code: str) -> bool:
    """Is this donor snippet something a model could actually be asked to use?

    The first run accepted whatever fell between two sentinels, so 16 of 37 cases handed the model
    0-1 real code lines: a bare comment, or a `def` line whose body held the next entity's sentinel
    and was cut off. Such a case cannot show adoption of anything, and pooling them produced a
    spurious +0.099 for Gemma. A usable snippet parses on its own and carries real code.
    """
    import ast
    import textwrap

    body = textwrap.dedent(code)
    if len([l for l in body.splitlines() if l.strip() and not l.strip().startswith("#")]) < 2:
        return False
    try:
        ast.parse(body)
    except SyntaxError:
        return False
    return True


def build_cases() -> list[dict]:
    """Frozen state + a failing entity + the correct code for it from a run that scored it 1.0."""
    import replay
    from substitution_probe import donors

    states = replay.best_states(ARMS_DIRS, 0.9)
    cases = []
    for name, state in sorted(states.items()):
        stem = Path(name).stem
        if not (MAPS / f"{stem}.pkl").exists():
            continue
        sm = pickle.loads((MAPS / f"{stem}.pkl").read_bytes())
        src = (getattr(sm, "source", "") or "").splitlines()
        code = donors(stem)
        for eid, ent in sm.entities.items():
            if eid not in code:
                continue
            span = getattr(ent, "source_span", None)
            start = getattr(span, "start_line", 0) if span else 0
            r_text = "\n".join(src[start:min(len(src), getattr(span, "end_line", start) + 1)]) if span else ""
            cases.append({"script": stem, "entity": eid, "source": state["source"],
                          "code": code[eid], "r_snippet": r_text})
    # Keep only entities the frozen state gets wrong: verifying each state once here (free, no model
    # calls) stops the arms spending calls on entities that already score 1.0.
    cache = OUT.parent / "cases.json"
    if cache.exists():
        want = {(c["script"], c["entity"]) for c in json.loads(cache.read_text(encoding="utf-8"))}
    else:
        from r2py import heldout as ho
        from r2py.harness.tools import HarnessTools
        from r2py.library import PatternLibrary
        manifest = ho.load_manifest(ROOT / "experiments/dev_run/manifest.json")
        cfg = manifest["protocol"]["translate"]
        want = set()
        by_state: dict = defaultdict(list)
        for c in cases:
            by_state[c["script"]].append(c)
        for stem, group in sorted(by_state.items()):
            sm = pickle.loads((MAPS / f"{stem}.pkl").read_bytes())
            tools = HarnessTools(sm, PatternLibrary(ROOT / "work/dev_run/checkpoints/empty"),
                                 model=cfg["model"], data_compare=cfg["data_compare"],
                                 timeout_s=cfg["timeout_s"], sidecar_filename=f"{stem}.r2py_data.json")
            tools.note_reference(group[0]["source"])
            rep = tools.verify(group[0]["source"])
            for c in group:
                es = rep.by_entity.get(c["entity"])
                if es is not None and ho.entity_score(es) <= 0.999:
                    want.add((stem, c["entity"]))
            print(f"   case prefilter: {stem[:40]:<42}{len([c for c in group if (stem, c['entity']) in want])}"
                  f"/{len(group)} entities below 1.0", flush=True)
    per_script: dict = {}
    kept = []
    for c in cases:                       # at most 4 failing entities per script, so none dominates
        if (c["script"], c["entity"]) not in want or not usable_guidance(c["code"]):
            continue
        n = per_script.get(c["script"], 0)
        if n < 4:
            per_script[c["script"]] = n + 1
            kept.append(c)
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps([{"script": c["script"], "entity": c["entity"]} for c in kept], indent=1),
                     encoding="utf-8")
    return kept


def summarise(rows: list[dict]) -> str:
    out = []
    for model in sorted({r.get("model", GEMMA) for r in rows}):
        out.append(_summarise_model([r for r in rows if r.get("model", GEMMA) == model], model))
    return ("\n" + "\n").join(out)


def _summarise_model(rows: list[dict], model: str) -> str:
    by: dict = defaultdict(list)
    for r in rows:
        by[r["treatment"]].append(r)
    lines = [f"{model}: {len(rows)} runs over {len({(r['script'], r['entity']) for r in rows})} cases",
             f"{'arm':<16}{'runs':>5}{'adoption':>10}{'entity before':>15}{'after':>8}"
             f"{'better':>8}{'worse':>7}{'action':>22}"]
    for t in TREATMENTS:
        rs = [r for r in by.get(t, []) if r.get("outcome") == "verified" and r.get("after") is not None]
        if not rs:
            lines.append(f"{t:<16}{len(by.get(t, [])):>5}   (none verified)")
            continue
        ad = [r["adoption"] for r in rs if r.get("adoption") is not None]
        acts = {}
        for r in by[t]:
            acts[r.get("action", "?")] = acts.get(r.get("action", "?"), 0) + 1
        lines.append(f"{t:<16}{len(rs):>5}{st.mean(ad) if ad else 0:>9.1%}"
                     f"{st.mean(r['before'] for r in rs):>15.3f}{st.mean(r['after'] for r in rs):>8.3f}"
                     f"{sum(1 for r in rs if r['after'] > r['before'] + 0.01):>8}"
                     f"{sum(1 for r in rs if r['after'] < r['before'] - 0.01):>7}"
                     f"   {','.join(f'{k}:{v}' for k, v in sorted(acts.items()))[:19]:>19}")
    # paired against the control, on the cases where both arms verified
    ctrl = {(r["script"], r["entity"], r["sample"]): r for r in by.get("none", [])
            if r.get("after") is not None}
    lines.append("")
    for t in TREATMENTS[1:]:
        pairs = [(r, ctrl[(r["script"], r["entity"], r["sample"])]) for r in by.get(t, [])
                 if r.get("after") is not None and (r["script"], r["entity"], r["sample"]) in ctrl]
        if not pairs:
            continue
        d = [a["after"] - b["after"] for a, b in pairs]
        lines.append(f"{t} - none, paired: n={len(d)}  mean {st.mean(d):+.3f}  "
                     f"better/worse {sum(1 for x in d if x > 0.01)}/{sum(1 for x in d if x < -0.01)}")
    return "\n".join(lines)


def main() -> int:
    from r2py.keepawake import keep_awake
    keep_awake()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--samples", type=int, default=1)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=None, help="smoke test: this many cases")
    ap.add_argument("--treatments", nargs="+", default=list(TREATMENTS))
    ap.add_argument("--models", nargs="+", default=[GEMMA],
                    help="agent models to compare (a control for the model factor)")
    ap.add_argument("--summary-only", action="store_true")
    args = ap.parse_args()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    done = [json.loads(l) for l in OUT.open(encoding="utf-8")] if OUT.exists() else []
    done = [r for r in done if r.get("outcome") != "provider_unavailable"]
    if args.summary_only:
        print(summarise(done))
        return 0
    cases = build_cases()
    if args.limit:
        cases = cases[:args.limit]
    finished = {(r["script"], r["entity"], r["treatment"], r["sample"], r.get("model", GEMMA))
                for r in done}
    tasks = [dict(c, treatment=t, sample=s, model=m)
             for s in range(args.samples) for c in cases for t in args.treatments for m in args.models
             if (c["script"], c["entity"], t, s, m) not in finished]
    print(f"{len(cases)} cases, {len(args.treatments)} arms, {len(args.models)} model(s), "
          f"{args.samples} sample(s): {len(tasks)} calls to make ({len(finished)} done)", flush=True)
    ctx = multiprocessing.get_context("spawn")
    outages = 0
    with ctx.Pool(args.workers) as pool, OUT.open("a", encoding="utf-8") as fh:
        for i, row in enumerate(pool.imap_unordered(run_one, tasks), start=1):
            if row.get("outcome") == "provider_unavailable":
                outages += 1
                print(f"[{i}/{len(tasks)}] provider unavailable ({row.get('provider')}): "
                      f"{row['script']} {row['entity']} {row['treatment']} — discarded", flush=True)
                if outages >= 3:
                    pool.terminate()
                    print(f"\nstopping: {outages} runs met a provider outage and were discarded. "
                          "Nothing partial was recorded; the same command resumes.", flush=True)
                    break
                continue
            fh.write(json.dumps(row) + "\n")
            fh.flush()
            done.append(row)
            print(f"[{i}/{len(tasks)}] {row['script'][:26]:<28}{row['entity'][:16]:<18}"
                  f"{row['treatment']:<16}{row['model'].split('/')[-1][:14]:<16}"
                  f"{row.get('before')} -> {row.get('after')}  "
                  f"adopt {row.get('adoption')}  {row.get('outcome', '')[:40]}", flush=True)
    print("\n" + summarise(done))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Does Gemma follow guidance less because of what it reads, what it must write, or neither? (registered 2026-10-11)

Each case is a frozen state plus one entity it gets wrong, with guidance that would fix it: the correct
code for that entity (snippet cases, from the prompt-arms rig) or R's exact printed output for it (print
cases). Every prompt ends with the same guidance block - a neutral canary instruction and the substantive
fix - and the arms vary only what precedes it and what the model must write:

  A1 full/whole    today's agent turn, answer the whole file
  A2 full/entity   today's agent turn, answer one entity (replace_entity)
  A3 trim/whole    R source, full Python, only this entity's scores/comparisons/feedback; whole file
  A4 trim/entity   as A3; one entity
  A5 local         this entity's R lines, Python lines, scores/comparisons/feedback; one entity
  A6 local_pad     A5 plus unrelated material (another script) up to A1's length; one entity
  A7 full_x2       A1 plus the same padding up to twice A1's length; whole file

One model call per case per arm per sample, the answer applied and verified. Gemma only.

    python scripts/prompt_load.py run --samples 3 --workers 6
    python scripts/prompt_load.py summary
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import multiprocessing
import pickle
import random
import re
import statistics as st
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from prompt_arms import ARMS_DIRS, GEMMA, IDENT, MAPS, distinctive, guidance_text  # noqa: E402

OUT = ROOT / "work" / "prompt_load"
ARMS = ("A1_full_whole", "A2_full_entity", "A3_trim_whole", "A4_trim_entity", "A5_local", "A6_local_pad",
        "A7_full_x2")
# Follow-up (2026-10-11): the system prompt crossed with the content, to separate what A2 vs A5 confounded.
FOLLOWUP = ("A2_full_entity", "A5_local", "B1_full_entity_shortsys", "B2_local_agentsys")
# Part A (2026-10-12): the system prompt varies, the turn is A1 (full turn, whole-file answer).
SYSPROMPT = ("S0_current", "S1_minimal", "S2_rules", "S3_no_tools", "S1a_follow", "S1b_follow_compute")
WHOLE = {"A1_full_whole", "A3_trim_whole", "A7_full_x2", *SYSPROMPT}
REQUIRE_RUNS = False   # Part A: only states whose starting program runs
LOCAL = {"A5_local", "A6_local_pad", "B2_local_agentsys"}
CASES_PER_SCRIPT = 3        # per kind
ADOPT_SNIPPET, ADOPT_PRINT = 0.5, 0.95


def _r_stdout(sm, eid: str) -> str:
    from r2py.stage1.runner import strip_echoed_source
    eb = (getattr(sm, "entity_bundles", {}) or {}).get(eid)
    return strip_echoed_source(getattr(eb, "stdout", "") or "").strip() if eb is not None else ""


def _tools(sm, stem):
    from r2py import heldout as ho
    from r2py.harness.tools import HarnessTools
    from r2py.library import PatternLibrary
    cfg = ho.load_manifest(ROOT / "experiments/dev_run/manifest.json")["protocol"]["translate"]
    return HarnessTools(sm, PatternLibrary(ROOT / "work/dev_run/checkpoints/empty"), model=cfg["model"],
                        data_compare=cfg["data_compare"], timeout_s=cfg["timeout_s"],
                        sidecar_filename=f"{stem}.r2py_data.json")


def _single_span(source: str, eid: str) -> bool:
    """An entity split over several places cannot be replaced as one block (splice_entity refuses), which
    would fail the one-entity arms for reasons that have nothing to do with the prompt (the smoke test:
    21 of the first 42 cases)."""
    from r2py.stage2.sentinel_mapper import ranges_from_sentinels
    return len(ranges_from_sentinels(source).get(eid, [])) == 1


def frozen_cases() -> list[dict]:
    """Snippet and print cases from the frozen states, by verifying each state once (no model calls)."""
    import replay
    from prompt_arms import usable_guidance
    from substitution_probe import donors
    # every dev state, not only the 20 replay states (start < 0.9): those hold only 20 single-span cases,
    # and a state that scores >= 0.9 overall still has entities it gets wrong
    states = replay.best_states(ARMS_DIRS, 1.01)
    out = []
    for name, state in sorted(states.items()):
        stem = Path(name).stem
        if not (MAPS / f"{stem}.pkl").exists():
            continue
        sm = pickle.loads((MAPS / f"{stem}.pkl").read_bytes())
        tools = _tools(sm, stem)
        tools.note_reference(state["source"])
        rep = tools.verify(state["source"])
        if REQUIRE_RUNS and rep.py_exit_code != 0:
            print(f"   cases: {stem[:44]:<46}start crashes, skipped", flush=True)
            continue
        code = donors(stem)
        src = (sm.source or "").splitlines()
        n = {"snippet": 0, "print": 0}
        for eid, es in rep.by_entity.items():
            if not _single_span(state["source"], eid):
                continue
            from r2py import heldout as ho
            if ho.entity_score(es) > 0.999:
                continue
            if eid in code and usable_guidance(code[eid]) and n["snippet"] < CASES_PER_SCRIPT:
                span = sm.entities[eid].source_span
                out.append({"script": stem, "entity": eid, "source": state["source"], "kind": "snippet",
                            "code": code[eid], "r_snippet": chr(10).join(src[span.start_line:span.end_line + 1])})
                n["snippet"] += 1
                continue
            dims = {d: getattr(es, d) for d in es.active_dims}
            r_out = _r_stdout(sm, eid)
            py_eb = (rep.py_entity_bundles or {}).get(eid)
            py_out = (getattr(py_eb, "stdout", "") or "").strip()
            if (n["print"] < CASES_PER_SCRIPT and es.executed_ok and r_out and py_out != r_out
                    and dims.get("side_effects", 1) < 0.9
                    and all(v >= 0.9 for d, v in dims.items() if d != "side_effects")):
                out.append({"script": stem, "entity": eid, "source": state["source"], "kind": "print",
                            "r_print": r_out[:3000]})
                n["print"] += 1
        print(f"   cases: {stem[:44]:<46}{n}", flush=True)
    return out


TRAIN_MAPS = ROOT / "work" / "reverify" / "script_maps"
TRAIN_SOURCES = ROOT / "work" / "heldout" / "train_outputs"
VALUE_MAX_CHARS = 1500       # a fitted model serialised to 20k characters is not usable guidance
TRAIN_PER_SCRIPT = 2


def _r_values(sm, eid: str) -> str:
    """R's values of the variables an entity assigns, as `name = <json>` lines ("" if none or too large)."""
    eb = (getattr(sm, "entity_bundles", {}) or {}).get(eid)
    data = getattr(eb, "data", None) or {}
    text = "\n".join(f"{k} = {json.dumps(v, default=str)}" for k, v in data.items())
    return text if 0 < len(text) <= VALUE_MAX_CHARS else ""


def training_cases() -> list[dict]:
    """Print and value cases from the training translations whose program runs (S1 refinement, 2026-10-12)."""
    from r2py import heldout as ho
    out = []
    for f in sorted(TRAIN_MAPS.glob("*.pkl")):
        stem = f.stem
        src_file = TRAIN_SOURCES / f"{stem}.py"
        if not src_file.exists():
            continue
        source = src_file.read_text(encoding="utf-8")
        sm = pickle.loads(f.read_bytes())
        tools = _tools(sm, stem)
        tools.note_reference(source)
        try:
            rep = tools.verify(source)
        except Exception as exc:                    # one bad script must not stop the pool
            print(f"   training: {stem[:44]:<46}verify failed: {exc}"[:120], flush=True)
            continue
        if rep.py_exit_code != 0:
            continue
        n = 0
        for eid, es in rep.by_entity.items():
            if n >= TRAIN_PER_SCRIPT or not es.executed_ok or not _single_span(source, eid):
                continue
            if ho.entity_score(es) > 0.9:
                continue
            dims = {d: getattr(es, d) for d in es.active_dims}
            value_dims = {d: v for d, v in dims.items() if d != "side_effects"}
            r_out = _r_stdout(sm, eid)
            py_eb = (rep.py_entity_bundles or {}).get(eid)
            py_out = (getattr(py_eb, "stdout", "") or "").strip()
            base = {"script": stem, "entity": eid, "source": source, "maps": str(TRAIN_MAPS)}
            if (r_out and py_out != r_out and dims.get("side_effects", 1) < 0.9
                    and all(v >= 0.9 for v in value_dims.values())):
                out.append(dict(base, kind="print", r_print=r_out[:3000]))
                n += 1
            elif value_dims and min(value_dims.values()) < 0.9 and (vals := _r_values(sm, eid)):
                out.append(dict(base, kind="value", r_values=vals))
                n += 1
        print(f"   training: {stem[:44]:<46}{n}", flush=True)
    return out


def sample_balanced(cases: list[dict], n: int, seed: int = 0) -> list[dict]:
    """``n`` cases, half of each kind as far as the pool allows, at most one per script and kind first."""
    rng = random.Random(seed)
    by_kind = defaultdict(list)
    for c in cases:
        by_kind[c["kind"]].append(c)
    picked = []
    for kind, cs in sorted(by_kind.items()):
        rng.shuffle(cs)
        first = {c["script"]: c for c in reversed(cs)}         # one per script before any second
        ordered = list(first.values()) + [c for c in cs if c not in first.values()]
        picked += ordered[:n // len(by_kind)]
    return picked


def all_cases() -> list[dict]:
    cache = OUT / "cases.json"
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    cases = frozen_cases()
    OUT.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(cases, indent=1), encoding="utf-8")
    return cases


def padding(stem: str, n_chars: int, states: dict) -> str:
    """Another script's R and Python, labelled unrelated, cut to ``n_chars`` (deterministic per case)."""
    others = sorted(n for n in states if Path(n).stem != stem)
    random.Random(stem).shuffle(others)
    chunks, size = [], 0
    for name in others * 3:
        s = states[name]
        block = (f"#### Unrelated script `{Path(name).stem}` (not part of this task; ignore it)\n"
                 f"```python\n{s['source']}\n```\n")
        chunks.append(block)
        size += len(block)
        if size >= n_chars:
            break
    text = "".join(chunks)[:max(0, n_chars)]
    return ("### Unrelated reference material (other scripts; not part of this task)\n" + text + "\n```\n\n"
            if n_chars > 0 else "")


def guidance(case: dict, token: str) -> str:
    eid = case["entity"]
    canary = (f"### Required marker\nPut this exact comment line inside the code of entity `{eid}`: "
              f"`# ack-{token}`")
    if case["kind"] == "snippet":
        fix = guidance_text(eid, case["code"], True)
    elif case["kind"] == "value":
        fix = ("### What R computes for this statement\n"
               f"When R runs entity `{eid}`, its variables hold these values (as JSON):\n```\n{case['r_values']}\n```\n"
               f"Make the Python for `{eid}` compute exactly these values from the data, the way R does "
               "(do not paste them as literals).")
    else:
        fix = ("### What R prints for this statement\n"
               f"When R runs entity `{eid}`, it prints exactly:\n```\n{case['r_print']}\n```\n"
               f"Make the Python for `{eid}` print exactly this text, with the same layout and formatting, "
               "computed from the data (not pasted as a literal).")
    return canary + "\n\n" + fix


def scope_text(arm: str, eid: str) -> str:
    head = "Do not probe R or look anything up: answer with code now.\n"
    if arm in WHOLE:
        return head + "Answer with ACTION: rewrite and the complete Python file."
    return head + (f"Answer with ACTION: replace_entity for this one entity (ENTITY: {eid}) and nothing else. "
                   "Do not rewrite the whole file.")


def build_prompt(arm: str, case: dict, sm, source: str, rep, states: dict, token: str) -> tuple[str, str]:
    """(system, user) for one arm."""
    from r2py import heldout as ho
    from r2py.harness.prompt import (AGENT_SYSTEM_PROMPT, ENTITY_REPAIR_SYSTEM, build_agent_turn,
                                     format_score_report, without_replace_entity)
    from r2py.stage2.sentinel_mapper import ranges_from_sentinels
    from r2py.stage2.stitch import hide_data_shim

    cfg = ho.load_manifest(ROOT / "experiments/dev_run/manifest.json")["protocol"]["translate"]
    stem, eid = case["script"], case["entity"]
    shown = hide_data_shim(source)
    full = build_agent_turn(sm.source or "", shown, rep, sm, 1, cfg["max_iters"], 10, history=[],
                            sidecar_filename=f"{stem}.r2py_data.json")[0]["content"]
    mine = dataclasses.replace(
        rep, by_entity={k: v for k, v in rep.by_entity.items() if k == eid},
        comparisons=[c for c in rep.comparisons if c.entity_id == eid],
        feedback=[f for f in rep.feedback if f.entity_id == eid])
    tail = "\n\n" + guidance(case, token) + "\n\n" + scope_text(arm, eid)
    # Sizes are total prompt sizes (system + user). The smoke test showed the 5,000-character agent system
    # prompt kept "local" at 6.7k against 9.4k for "full", so the local arms get the harness's own
    # one-entity system prompt, and the padded arms are padded to A1's total and twice it.
    a1_total = len(without_replace_entity(AGENT_SYSTEM_PROMPT)) + len(full) + len(tail)
    if arm in ("A1_full_whole", "A2_full_entity", "B1_full_entity_shortsys", *SYSPROMPT):
        body = full
    elif arm == "A7_full_x2":
        body = padding(stem, a1_total, states) + full
    elif arm in ("A3_trim_whole", "A4_trim_entity"):
        body = "\n".join(["## Step 1", "", "### R source", "```r", sm.source or "", "```", "",
                          f"### Current Python translation ({len(shown.splitlines())} lines)", "```python", shown,
                          "```", "", "### Verification result (this entity)", format_score_report(mine)])
    else:
        ent = sm.entities[eid]
        span = ent.source_span
        r_lines = "\n".join((sm.source or "").splitlines()[span.start_line:span.end_line + 1])
        lines = source.splitlines()
        py_lines = "\n".join(l for a, b in ranges_from_sentinels(source).get(eid, []) for l in lines[a:b + 1]
                             if "r2py:entity:" not in l)
        body = "\n".join([f"## Entity `{eid}`", "", "### R code of this entity", "```r", r_lines, "```", "",
                          "### Current Python code of this entity", "```python", py_lines, "```", "",
                          "### Verification result (this entity)", format_score_report(mine)])
        if arm == "A6_local_pad":
            body = padding(stem, a1_total - len(ENTITY_REPAIR_SYSTEM) - len(body) - len(tail), states) + body
    if arm in SYSPROMPT:
        from sysprompt_variants import variants
        system = variants()[arm]
    elif arm == "B2_local_agentsys":
        system = AGENT_SYSTEM_PROMPT
    elif arm in LOCAL or arm == "B1_full_entity_shortsys":
        system = ENTITY_REPAIR_SYSTEM
    else:
        system = without_replace_entity(AGENT_SYSTEM_PROMPT) if arm in WHOLE else AGENT_SYSTEM_PROMPT
    return system, body + tail


def run_one(task: dict) -> dict:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    from r2py import heldout as ho
    from r2py.harness.agent import _parse_action
    from r2py.stage2 import llm
    from r2py.stage2.sentinel_mapper import ranges_from_sentinels
    from r2py.stage2.stitch import show_data_shim, splice_entity
    from r2py.harness.objective import entity_status
    from r2py.stage4.comparators.stdout import StdoutComparator
    import replay

    case, arm = task["case"], task["arm"]
    stem, eid = case["script"], case["entity"]
    row = {"script": stem, "entity": eid, "kind": case["kind"], "arm": arm, "sample": task["sample"]}
    started = time.monotonic()
    calls = [0]
    real = llm.call

    def counted(*a, **k):
        calls[0] += 1
        return real(*a, **k)
    try:
        manifest = ho.load_manifest(ROOT / "experiments/dev_run/manifest.json")
        sm = pickle.loads((Path(case.get("maps", MAPS)) / f"{stem}.pkl").read_bytes())
        tools = _tools(sm, stem)
        source = case["source"]
        tools.note_reference(source)
        states = replay.best_states(ARMS_DIRS, 0.9)
        token = f"{random.Random(f'{stem}{eid}{arm}{task['sample']}').getrandbits(24):06x}"
        with ho.pinned_llm(GEMMA, ho.llm_settings(manifest)):
            llm.call = counted
            base = tools.verify(source)
            row["before"] = round(ho.entity_score(base.by_entity[eid]), 4)
            row["start_runs"] = base.py_exit_code == 0          # a crashing start blocks what follows the crash
            row["status_before"] = entity_status(base, eid)
            r_out = _r_stdout(sm, eid)
            py_eb = (base.py_entity_bundles or {}).get(eid)
            if case["kind"] == "print":
                row["print_before"] = round(StdoutComparator().compare(
                    r_out, (getattr(py_eb, "stdout", "") or "").strip()).score, 4)
            system, user = build_prompt(arm, case, sm, source, base, states, token)
            row["prompt_chars"] = len(system) + len(user)
            raw = llm.call([{"role": "user", "content": user}], system, model=GEMMA, max_tokens=16384)
        row["canary_anywhere"] = f"ack-{token}" in raw
        action = _parse_action(raw)
        row["action"] = (action or {}).get("action", "(unparsed)")
        new_source = (action or {}).get("new_source")
        if not new_source:
            row["outcome"] = "no code"
            return row
        # A local arm shows only the entity, so whatever action it names, its code is that entity's code.
        if row["action"] in ("replace_entity", "entity_repair") or arm in LOCAL:
            spliced, err = splice_entity(source, (action or {}).get("entity", "") or eid, new_source)
            if spliced is None:
                row["outcome"] = f"splice refused: {err[:80]}"
                return row
            new_source = spliced
        new_source = show_data_shim(source, new_source)
        lines = new_source.splitlines()
        got = "\n".join(l for a, b in ranges_from_sentinels(new_source).get(eid, []) for l in lines[a:b + 1])
        row["canary_in_entity"] = f"ack-{token}" in got
        if arm in SYSPROMPT:
            # Part A gates: does a shorter system prompt bring back what its rules were written against?
            from r2py.harness.agent import _check_syntax
            from r2py.harness.review import review_translation
            from r2py.stage2.stitch import sanitize_keyword_args
            row["syntax_error"] = _check_syntax(new_source) is not None
            row["arg_order_fixes"] = len(sanitize_keyword_args(new_source)[1])
            with ho.pinned_llm(GEMMA, ho.llm_settings(manifest)):
                llm.call = counted
                passed, reason = review_translation(sm.source or "", new_source, sm, model=GEMMA)
                llm.call = real
            row["review_rejected"] = not passed
            row["review_reason"] = (reason or "")[:200]
        rep = tools.verify(new_source)
        after = rep.by_entity.get(eid)
        row["after"] = round(ho.entity_score(after), 4) if after else None
        row["status_after"] = entity_status(rep, eid)
        row["aggregate_before"], row["aggregate_after"] = round(base.aggregate, 4), round(rep.aggregate, 4)
        row["exit_after"] = rep.py_exit_code
        if case["kind"] == "snippet":
            want = distinctive(case["code"], case.get("r_snippet", ""))
            row["adoption"] = round(len(want & set(IDENT.findall(got))) / len(want), 4) if want else None
            row["adopted"] = row["adoption"] is not None and row["adoption"] >= ADOPT_SNIPPET
        elif case["kind"] == "value":
            # adopted = R's values reproduced (the entity's value dimensions); like print adoption, part of the score
            vd = [getattr(after, d) for d in after.active_dims if d != "side_effects"] if after and after.executed_ok else []
            row["adoption"] = round(min(vd), 4) if vd else 0.0
            row["adopted"] = bool(vd) and min(vd) >= ADOPT_PRINT
            nums = set(re.findall(r"-?\d+\.\d{3,}", case["r_values"]))
            row["pasted_literal"] = len(nums) >= 3 and sum(n in got for n in nums) >= 3
        else:
            py_eb = (rep.py_entity_bundles or {}).get(eid)
            sim = StdoutComparator().compare(r_out, (getattr(py_eb, "stdout", "") or "").strip()).score
            row["adoption"] = round(sim, 4)
            row["adopted"] = sim >= ADOPT_PRINT
            # pasting R's output as a literal is not following the instruction "computed from the data"
            first = next((l.strip() for l in r_out.splitlines() if len(l.strip()) > 12), "")
            row["pasted_literal"] = bool(first) and first in got
        row["entity_code"] = got[:2000]
        row["outcome"] = "verified"
    except Exception as exc:
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


def run(samples: int, workers: int, only_arms: list[str] | None = None) -> None:
    cases = all_cases()
    path = OUT / "results.jsonl"
    done = [json.loads(l) for l in path.open(encoding="utf-8")] if path.exists() else []
    finished = {(r["script"], r["entity"], r["arm"], r["sample"]) for r in done
                if r.get("outcome") != "provider_unavailable"}
    arms = only_arms or list(ARMS)
    tasks = [{"case": c, "arm": a, "sample": s} for s in range(samples) for c in cases for a in arms
             if (c["script"], c["entity"], a, s) not in finished]
    print(f"{len(cases)} cases ({sum(c['kind'] == 'snippet' for c in cases)} snippet, "
          f"{sum(c['kind'] == 'print' for c in cases)} print), {len(arms)} arms, {samples} samples: "
          f"{len(tasks)} calls to do, {workers} workers", flush=True)
    outages = 0
    with multiprocessing.get_context("spawn").Pool(workers) as pool, path.open("a", encoding="utf-8") as fh:
        for i, row in enumerate(pool.imap_unordered(run_one, tasks), 1):
            fh.write(json.dumps(row) + "\n")
            fh.flush()
            outages += row.get("outcome") == "provider_unavailable"
            print(f"[{i}/{len(tasks)}] {row['script'][:30]:<32}{row['entity'][:16]:<18}{row['arm']:<16}"
                  f"s{row['sample']} {row.get('outcome', '')[:30]:<30} canary={row.get('canary_in_entity')} "
                  f"adopted={row.get('adopted')} {row.get('before')}->{row.get('after')}", flush=True)
            if outages >= 3:
                print("3 provider outages: stopping; the same command resumes", flush=True)
                pool.terminate()
                break


def summary() -> str:
    rows = [json.loads(l) for l in (OUT / "results.jsonl").open(encoding="utf-8")]
    rows = [r for r in rows if r.get("outcome") != "provider_unavailable"]
    text = _table(rows, f"{len(rows)} calls (provider outages excluded)")
    if any("start_runs" in r for r in rows):
        # An upstream crash nullifies whatever is done to the entity: report the cases that can show an effect.
        runs = [r for r in rows if r.get("start_runs")]
        text += "\n\n" + _table(runs, f"cases whose starting program runs: {len(runs)} calls; outcomes blocked "
                                       f"by an earlier crash afterwards: "
                                       f"{sum(r.get('status_after') == 'blocked' for r in runs)}")
    return text


def _table(rows: list[dict], title: str) -> str:
    lines = [title]
    by = defaultdict(list)
    for r in rows:
        by[r["arm"]].append(r)
    hdr = f"{'arm':<16}{'n':>4}{'chars':>8}{'no code':>9}{'canary':>8}{'adopt':>7}{'adopt snip':>11}{'adopt prnt':>11}{'d score':>9}"
    lines.append(hdr)
    for arm in ARMS + FOLLOWUP[2:] + SYSPROMPT:
        rs = by.get(arm, [])
        if not rs:
            continue

        def rate(xs):
            return f"{sum(xs) / len(xs):.0%}" if xs else "-"
        verified = [r for r in rs if r.get("outcome") == "verified"]
        lines.append(
            f"{arm:<16}{len(rs):>4}{st.median(r.get('prompt_chars', 0) for r in rs):>8.0f}"
            f"{rate([r.get('outcome') == 'no code' for r in rs]):>9}"
            f"{rate([bool(r.get('canary_in_entity')) for r in rs]):>8}"
            f"{rate([bool(r.get('adopted')) for r in rs]):>7}"
            f"{rate([bool(r.get('adopted')) for r in rs if r['kind'] == 'snippet']):>11}"
            f"{rate([bool(r.get('adopted')) for r in rs if r['kind'] == 'print']):>11}"
            f"{st.mean((r['after'] or 0) - r['before'] for r in verified) if verified else 0:>+9.3f}")
    lines.append("(rates over all calls: no code / refused splices count as not following; "
                 "print cases that pasted R's output as a literal: "
                 f"{sum(bool(r.get('pasted_literal')) for r in rows)})")
    return "\n".join(lines)


def main() -> int:
    from r2py.keepawake import keep_awake
    keep_awake()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("run")
    p.add_argument("--samples", type=int, default=3)
    p.add_argument("--workers", type=int, default=6)
    p.add_argument("--arms", nargs="+", choices=ARMS + FOLLOWUP[2:] + SYSPROMPT)
    sub.add_parser("cases")
    sub.add_parser("summary")
    for q in (p, sub.choices["summary"], sub.choices["cases"]):
        q.add_argument("--tag", default="", help="separate results directory (cases are copied from the main run)")
    for q in (p, sub.choices["cases"]):
        q.add_argument("--require-runs", action="store_true",
                       help="build fresh cases from states whose starting program runs (Part A)")
    sub.choices["cases"].add_argument("--training", type=int, default=0,
                                      help="sample this many print/value cases from the training translations")
    args = ap.parse_args()
    global OUT, REQUIRE_RUNS
    REQUIRE_RUNS = getattr(args, "require_runs", False)
    if getattr(args, "tag", ""):
        tagged = OUT.with_name(f"{OUT.name}_{args.tag}")
        tagged.mkdir(parents=True, exist_ok=True)
        if not (tagged / "cases.json").exists() and not REQUIRE_RUNS and not getattr(args, "training", 0):
            (tagged / "cases.json").write_text((OUT / "cases.json").read_text(encoding="utf-8"), encoding="utf-8")
        OUT = tagged
    if args.cmd == "cases" and getattr(args, "training", 0):
        pool = training_cases()
        cs = sample_balanced(pool, args.training)
        (OUT / "pool.json").write_text(json.dumps(pool, indent=1), encoding="utf-8")
        (OUT / "cases.json").write_text(json.dumps(cs, indent=1), encoding="utf-8")
        kinds = lambda xs: {k: sum(c["kind"] == k for c in xs) for k in ("print", "value")}  # noqa: E731
        print(f"pool {len(pool)} {kinds(pool)}; sampled {len(cs)} {kinds(cs)} from "
              f"{len({c['script'] for c in cs})} scripts")
        return 0
    if args.cmd == "cases":
        cs = all_cases()
        print(f"{len(cs)} cases: {sum(c['kind'] == 'snippet' for c in cs)} snippet, "
              f"{sum(c['kind'] == 'print' for c in cs)} print")
        return 0
    if args.cmd == "run":
        run(args.samples, args.workers, args.arms)
    text = summary()
    print("\n" + text)
    (OUT / "summary.txt").write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

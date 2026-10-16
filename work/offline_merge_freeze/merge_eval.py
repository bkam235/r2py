"""Offline ceiling of per-entity acceptance (option 1) and freezing verified entities (option 2)."""
import json, glob, sys, collections, pickle
from pathlib import Path
ROOT = Path("C:/Users/bened/Desktop/r2py_v0.3"); sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from r2py.stage2.sentinel_mapper import restore_sentinels, ranges_from_sentinels
from r2py.stage2.stitch import splice_entity
import replay
STATES = replay.best_states([str(ROOT / f"work/smoke/{a}") for a in ("20261001_112951", "20261001_140509", "20261001_165951")], 0.9)
FILES = sorted(glob.glob(str(ROOT / "work/replay_sysprompt/trajectories/*.rewrite_w3.[0-9].jsonl"))) + \
        sorted(glob.glob(str(ROOT / "work/replay_feedback/trajectories/*.rewrite_w3.[0-9].jsonl")))
VER, GAIN = 0.95, 0.05
START = json.loads(Path(__file__).with_name("start_scores.json").read_text()) if Path(__file__).with_name("start_scores.json").exists() else {}

def body(src, eid):
    sp = ranges_from_sentinels(src).get(eid) or []
    if len(sp) != 1: return None
    a, b = sp[0]; L = src.splitlines()
    return "\n".join(l for l in L[a:b + 1] if "r2py:entity:" not in l)

def splice_many(target, donor, eids):
    out = target
    for e in eids:
        bd = body(donor, e)
        if bd is None: return None
        out, err = splice_entity(out, e, bd)
        if out is None: return None
    return out

def steps():
    """(script, base_src, base_pe, base_agg, cand_src, cand_pe, cand_agg, accepted) per candidate, in loop order."""
    for f in FILES:
        ev = [json.loads(l) for l in open(f, encoding="utf-8")]
        script = ev[0]["script"]; start = STATES[script]["source"]
        acc = {(e.get("branch"), e["step"]) for e in ev if e["kind"] == "accepted"}
        by_branch = collections.defaultdict(list)
        for e in ev:
            if e["kind"] == "step" and e.get("source") and e.get("per_entity") is not None:
                by_branch[e.get("branch")].append(e)
        for br, es in by_branch.items():
            st0 = START.get(script, {})
            base, base_pe, base_agg = start, st0.get("pe"), st0.get("agg")
            seen = set()
            for e in sorted(es, key=lambda x: x["step"]):
                if e["step"] in seen: continue           # one candidate per step (outcome events repeat)
                seen.add(e["step"])
                cand = restore_sentinels(base, e["source"])
                yield dict(file=Path(f).name, script=script, base=base, base_pe=base_pe, base_agg=base_agg,
                           cand=cand, cand_pe=e["per_entity"], cand_agg=e.get("aggregate"),
                           accepted=(br, e["step"]) in acc,
                           native=set(ranges_from_sentinels(base)) <= set(ranges_from_sentinels(e["source"])))
                if (br, e["step"]) in acc:
                    base, base_pe, base_agg = cand, e["per_entity"], e.get("aggregate")

if __name__ == "__main__" and sys.argv[1] == "count":
    c = collections.Counter(); kept = []
    for s in steps():
        c["candidates"] += 1
        if s["base_pe"] is None: c["first step of a branch (base scores unknown offline)"] += 1; continue
        deg = [e for e, v in s["base_pe"].items() if v >= VER and s["cand_pe"].get(e, 0) < VER]
        imp = [e for e, v in s["cand_pe"].items() if v > s["base_pe"].get(e, 0) + GAIN]
        if deg: c["damages a verified entity"] += 1
        if imp and not s["accepted"]: c["rejected but improves some entity"] += 1
        if deg and s["accepted"]: c["accepted although it damaged a verified entity"] += 1
        if deg and body(s["base"], deg[0]) is not None: c["freeze applicable (spliceable)"] += 1
        if imp and not s["accepted"] and splice_many(s["base"], s["cand"], imp) is not None: c["merge applicable (spliceable)"] += 1
    for k, v in c.items(): print(f"{v:>6}  {k}")


def _verify_case(case):
    from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=True)
    from prompt_load import _tools
    from r2py.harness import objective as obj
    try:
        stem = Path(case["script"]).stem
        sm = pickle.loads((ROOT / "work/replay/script_maps" / f"{stem}.pkl").read_bytes())
        out = {k: case[k] for k in ("file", "script", "option", "accepted", "n_entities")}
        reps = {}
        for k in ("base", "cand", "variant"):
            t = _tools(sm, stem); t.note_reference(case["base"]); reps[k] = t.verify(case[k])
            out[k] = round(reps[k].aggregate, 4); out[k + "_exit"] = reps[k].py_exit_code
        b, c, v = reps["base"], reps["cand"], reps["variant"]
        loop_next = c if obj.better(c, b) else b                     # what the loop held after this step
        out["loop_gain"] = round(loop_next.aggregate - b.aggregate, 4)
        best_with = v if obj.better(v, loop_next) else loop_next      # the option adds a candidate; the verifier picks
        out["option_gain"] = round(best_with.aggregate - b.aggregate, 4)
        return out
    except Exception as exc:
        return {"file": case["file"], "option": case["option"], "error": f"{type(exc).__name__}: {exc}"[:200]}


if __name__ == "__main__" and sys.argv[1] == "verify":
    import multiprocessing
    cases = []
    for s in steps():
        if s["base_pe"] is None: continue
        deg = [e for e, v in s["base_pe"].items() if v >= VER and s["cand_pe"].get(e, 0) < VER]
        imp = [e for e, v in s["cand_pe"].items() if v > s["base_pe"].get(e, 0) + GAIN]
        if deg:
            fr = splice_many(s["cand"], s["base"], deg)
            if fr is not None:
                cases.append(dict(s, option="freeze", variant=fr, n_entities=len(deg)))
        if imp and not s["accepted"]:
            mg = splice_many(s["base"], s["cand"], imp)
            if mg is not None:
                cases.append(dict(s, option="merge", variant=mg, n_entities=len(imp)))
    print(len(cases), "cases", flush=True)
    with multiprocessing.get_context("spawn").Pool(6) as p:
        res = p.map(_verify_case, cases)
    Path(sys.argv[2]).write_text(json.dumps(res), encoding="utf-8")
    import statistics as st
    for opt in ("freeze", "merge"):
        r = [x for x in res if x.get("option") == opt and "error" not in x]
        extra = [x["option_gain"] - x["loop_gain"] for x in r]
        print(f"{opt}: {len(r)} cases ({sum('error' in x for x in res if x.get('option') == opt)} errors); "
              f"option beats the loop's step in {sum(e > 0.005 for e in extra)}; "
              f"mean extra gain per case {st.mean(extra):+.4f}, sum {sum(extra):+.2f}; "
              f"variant crashes {sum(x['variant_exit'] != 0 for x in r)}")


def _crash_case(case):
    """The Python error of a merged variant, for the dependency diagnosis."""
    from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=True)
    import json as _j
    from r2py.stage2.sentinel_mapper import strip_sentinels, flatten_entity_line_map
    import r2py.stage4.verifier as V
    try:
        stem = Path(case["script"]).stem
        sm = pickle.loads((ROOT / "work/replay/script_maps" / f"{stem}.pkl").read_bytes())
        cfg = _j.load(open(ROOT / "experiments/dev_run/manifest.json"))["protocol"]["translate"]
        src = case["variant"]
        rep, b = V.verify(sm, strip_sentinels(src), data_compare=cfg["data_compare"],
                          entity_line_map=flatten_entity_line_map(ranges_from_sentinels(src)),
                          sidecar_filename=f"{stem}.r2py_data.json", timeout_s=cfg["timeout_s"], return_bundle=True)
        return {"file": case["file"], "script": case["script"], "exit": b.exit_code, "stderr": (b.stderr or "")[-1500:],
                "improved": case["improved"]}
    except Exception as exc:
        return {"file": case["file"], "error": str(exc)[:200]}


if __name__ == "__main__" and sys.argv[1] == "crashes":
    import multiprocessing
    cases = []
    for s in steps():
        if s["base_pe"] is None or s["accepted"]: continue
        imp = [e for e, v in s["cand_pe"].items() if v > s["base_pe"].get(e, 0) + GAIN]
        mg = splice_many(s["base"], s["cand"], imp) if imp else None
        if mg is not None:
            cases.append(dict(file=s["file"], script=s["script"], variant=mg, improved=imp))
    with multiprocessing.get_context("spawn").Pool(6) as p:
        res = p.map(_crash_case, cases)
    Path(sys.argv[2]).write_text(json.dumps(res), encoding="utf-8")
    print(len(res), "merged variants;", sum(r.get("exit") not in (0, None) for r in res), "crash")


# ---- connected change sets (2026-10-16) ------------------------------------------------------------------------
import ast as _ast
from r2py.stage2.stitch import hide_data_shim as _hide


def _units(src):
    """Top-level statements of src, each with the entity it belongs to (None = outside every entity), the names it
    defines and the names it loads."""
    rg = ranges_from_sentinels(src)
    owner = {}
    for eid, spans in rg.items():
        for a, b in spans:
            for ln in range(a, b + 1):
                owner[ln] = eid
    try:
        tree = _ast.parse(_hide(src))
    except SyntaxError:
        return None
    lines = src.splitlines()
    out = []
    for node in tree.body:
        defs, uses = set(), set()
        if isinstance(node, (_ast.FunctionDef, _ast.ClassDef, _ast.AsyncFunctionDef)):
            defs.add(node.name)
        for n in _ast.walk(node):
            if isinstance(n, _ast.Name):
                (uses if isinstance(n.ctx, _ast.Load) else defs).add(n.id)
            elif isinstance(n, (_ast.Import, _ast.ImportFrom)):
                defs |= {(a.asname or a.name).split(".")[0] for a in n.names}
        text = "\n".join(lines[node.lineno - 1:node.end_lineno])
        out.append(dict(owner=owner.get(node.lineno - 1), defs=defs, uses=uses - defs, text=text.strip(),
                        line=node.lineno))
    return out


def closure(base, cand, improved):
    """Entities and outside-entity statements of cand connected to the improved entities by def-use, whose text
    differs from base: the change set that has to move together."""
    cu, bu = _units(cand), _units(base)
    if cu is None or bu is None:
        return None, None
    base_texts = {u["text"] for u in bu}
    changed = [u for u in cu if u["text"] not in base_texts]
    ents, outside = set(improved), []
    frontier = [u for u in cu if u["owner"] in ents]
    seen = set()
    while frontier:
        u = frontier.pop()
        for name in u["uses"]:
            for d in changed:
                if name in d["defs"] and id(d) not in seen:
                    seen.add(id(d))
                    if d["owner"] is None:
                        outside.append(d)
                    elif d["owner"] not in ents:
                        ents.add(d["owner"])
                    frontier.append(d)
                    frontier += [x for x in cu if x["owner"] == d["owner"] and d["owner"] is not None]
    return ents, outside


def closure_merge(base, cand, improved):
    ents, outside = closure(base, cand, improved)
    if ents is None:
        return None, None
    merged = splice_many(base, cand, sorted(ents))
    if merged is None:
        return None, ents
    if outside:     # candidate-only helpers and imports go in before the first entity marker
        L = merged.splitlines()
        first = next((i for i, l in enumerate(L) if l.startswith("# r2py:entity:")), len(L))
        merged = "\n".join(L[:first] + [u["text"] for u in sorted(outside, key=lambda u: u["line"])] + [""] + L[first:])
    return merged, ents


if __name__ == "__main__" and sys.argv[1] == "closure":
    import multiprocessing, statistics as st
    cases, sizes = [], []
    for s in steps():
        if s["base_pe"] is None or s["accepted"]: continue
        imp = [e for e, v in s["cand_pe"].items() if v > s["base_pe"].get(e, 0) + GAIN]
        if not imp: continue
        mg, ents = closure_merge(s["base"], s["cand"], imp)
        if mg is not None:
            cases.append(dict(s, option="closure", variant=mg, n_entities=len(ents)))
            sizes.append((len(imp), len(ents)))
    print(len(cases), "closure merges (", sum(1 for a, b in sizes if b > a), "grew beyond the improved entities )", flush=True)
    with multiprocessing.get_context("spawn").Pool(6) as p:
        res = p.map(_verify_case, cases)
    Path(sys.argv[2]).write_text(json.dumps(res), encoding="utf-8")
    r = [x for x in res if "error" not in x]
    extra = [x["option_gain"] - x["loop_gain"] for x in r]
    print(f"closure: {len(r)} cases; variant crashes {sum(x['variant_exit'] != 0 for x in r)}; "
          f"beats the loop's step in {sum(e > 0.005 for e in extra)}; mean extra {st.mean(extra):+.4f}, sum {sum(extra):+.2f}; "
          f"scripts with a win {sorted({x['script'][:24] for x, e in zip(r, extra) if e > 0.005})}")


if __name__ == "__main__" and sys.argv[1] == "closure_crashes":
    import multiprocessing, re as _re, collections as _c
    cases = []
    for s in steps():
        if s["base_pe"] is None or s["accepted"]: continue
        imp = [e for e, v in s["cand_pe"].items() if v > s["base_pe"].get(e, 0) + GAIN]
        if not imp: continue
        mg, ents = closure_merge(s["base"], s["cand"], imp)
        if mg is not None:
            cases.append(dict(file=s["file"], script=s["script"], variant=mg, improved=imp, base=s["base"], cand=s["cand"]))
    with multiprocessing.get_context("spawn").Pool(6) as p:
        res = p.map(_crash_case, cases)
    kinds = _c.Counter(); ex = _c.defaultdict(list)
    for c, r in zip(cases, res):
        if r.get("exit") in (0, None): continue
        err = r["stderr"].strip().splitlines()
        last = err[-1] if err else "(none)"
        k = last.split(":")[0]
        # where in the merged program: the line the traceback names, and which entity it belongs to
        lines = [l for l in err if 'File "' in l and "_r2py_script.py" in l]
        kinds[k] += 1
        if len(ex[k]) < 6:
            ex[k].append((c["script"][:24], c["improved"][:2], last[:120], lines[-1].strip()[-40:] if lines else ""))
    print(kinds.most_common())
    for k, v in ex.items():
        print("==", k)
        for e in v: print("   ", e)
    Path(sys.argv[2]).write_text(json.dumps([dict(r, improved=c["improved"]) for c, r in zip(cases, res)]), encoding="utf-8")


if __name__ == "__main__" and sys.argv[1] == "native":
    # Which merge cases have candidates whose markers the model kept itself (no restoration needed)?
    import json as _j
    raw_markers = {}
    for f in FILES:
        for l in open(f, encoding="utf-8"):
            e = _j.loads(l)
            if e["kind"] == "step" and e.get("source"):
                raw_markers[(Path(f).name, e.get("branch"), e["step"])] = set(ranges_from_sentinels(e["source"]))
    cl = {(x["file"], tuple(x["improved"])): x for x in _j.load(open(Path(__file__).with_name("closure_crashes.json")))}
    tot = keep = 0; crash_keep = crash_restored = n_restored = 0
    for f in FILES:
        ev = [_j.loads(l) for l in open(f, encoding="utf-8")]
    for s in steps():
        if s["base_pe"] is None or s["accepted"]: continue
        imp = tuple(e for e, v in s["cand_pe"].items() if v > s["base_pe"].get(e, 0) + GAIN)
        x = cl.get((s["file"], imp))
        if not x: continue
        tot += 1
        native = set(ranges_from_sentinels(s["cand"])) <= set(ranges_from_sentinels(s["cand"]))  # placeholder
    print("see below")


if __name__ == "__main__" and sys.argv[1] == "native_merge":
    # Only candidates that kept every entity marker themselves: no restored (approximate) boundaries.
    import multiprocessing, statistics as st, collections as _c
    cnt = _c.Counter(); cases = []
    for s in steps():
        if s["base_pe"] is None or s["accepted"]: continue
        imp = [e for e, v in s["cand_pe"].items() if v > s["base_pe"].get(e, 0) + GAIN]
        if not imp: continue
        cnt["rejected but improving"] += 1
        cnt["native markers" if s["native"] else "restored markers"] += 1
        if not s["native"]: continue
        for opt, fn in (("merge", lambda: (splice_many(s["base"], s["cand"], imp), None)),
                        ("closure", lambda: closure_merge(s["base"], s["cand"], imp))):
            mg, _ = fn()
            if mg is not None:
                cases.append(dict(s, option=opt, variant=mg, n_entities=len(imp)))
    print(dict(cnt), len(cases), "native cases", flush=True)
    with multiprocessing.get_context("spawn").Pool(6) as p:
        res = p.map(_verify_case, cases)
    Path(sys.argv[2]).write_text(json.dumps(res), encoding="utf-8")
    for opt in ("merge", "closure"):
        r = [x for x in res if x.get("option") == opt and "error" not in x]
        if not r: continue
        extra = [x["option_gain"] - x["loop_gain"] for x in r]
        print(f"{opt}: {len(r)} native cases; variant crashes {sum(x['variant_exit'] != 0 for x in r)} "
              f"(candidate itself crashes in {sum(x['cand_exit'] != 0 for x in r)}); beats the loop's step in "
              f"{sum(e > 0.005 for e in extra)}; mean extra {st.mean(extra):+.4f}")


def _api(src):
    try:
        t = _ast.parse(_hide(src))
    except SyntaxError:
        return None
    return {n.name: tuple(a.arg for a in n.args.args) if isinstance(n, _ast.FunctionDef) else ("class",)
            for n in _ast.walk(t) if isinstance(n, (_ast.FunctionDef, _ast.ClassDef)) and n.col_offset == 0}


if __name__ == "__main__" and sys.argv[1] == "api_split":
    import multiprocessing, statistics as st
    cases = []
    for s in steps():
        if s["base_pe"] is None or s["accepted"]: continue
        imp = [e for e, v in s["cand_pe"].items() if v > s["base_pe"].get(e, 0) + GAIN]
        if not imp: continue
        a, b = _api(s["base"]), _api(s["cand"])
        if a is None or b is None or (not a and not b): continue
        mg = splice_many(s["base"], s["cand"], imp)
        if mg is not None:
            cases.append(dict(s, option="API unchanged" if a == b else "API changed", variant=mg, n_entities=len(imp)))
    with multiprocessing.get_context("spawn").Pool(6) as p:
        res = p.map(_verify_case, cases)
    Path(sys.argv[2]).write_text(json.dumps(res), encoding="utf-8")
    for opt in ("API unchanged", "API changed"):
        r = [x for x in res if x.get("option") == opt and "error" not in x]
        extra = [x["option_gain"] - x["loop_gain"] for x in r]
        print(f"{opt}: {len(r)} merges; merged program runs in {sum(x['variant_exit'] == 0 for x in r)} "
              f"(best state runs in {sum(x['base_exit'] == 0 for x in r)}, candidate in {sum(x['cand_exit'] == 0 for x in r)}); "
              f"beats the loop's step in {sum(e > 0.005 for e in extra)}; mean extra {st.mean(extra) if extra else 0:+.4f}")


if __name__ == "__main__" and sys.argv[1] == "api_same_errors":
    import multiprocessing
    cases = []
    for s in steps():
        if s["base_pe"] is None or s["accepted"]: continue
        imp = [e for e, v in s["cand_pe"].items() if v > s["base_pe"].get(e, 0) + GAIN]
        if not imp: continue
        a, b = _api(s["base"]), _api(s["cand"])
        if a is None or b is None or not a or a != b: continue
        mg = splice_many(s["base"], s["cand"], imp)
        if mg is not None:
            cases.append(dict(file=s["file"], script=s["script"], variant=mg, improved=imp))
    with multiprocessing.get_context("spawn").Pool(6) as p:
        res = p.map(_crash_case, cases)
    for c, r in zip(cases, res):
        if r.get("exit") in (0, None): continue
        err = [l for l in r["stderr"].strip().splitlines() if l.strip()]
        loc = [l.strip() for l in err if l.strip().startswith("File") and "_r2py_script.py" in l]
        print(f"{c['script'][:30]:<32}{c['improved'][:2]} {err[-1][:110] if err else ''} | {err[-2].strip()[:80] if len(err) > 1 else ''}")

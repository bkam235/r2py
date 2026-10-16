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
                           accepted=(br, e["step"]) in acc)
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

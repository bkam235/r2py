"""Graphics bet, kill test part 1 (2026-11-16, offline): for the default's epoch-14 finals of the states losing on
graphics, dump each losing entity's R and Python plot fingerprints (page count, keys, sizes, ranges, texts)."""
import json, pickle, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=True)
import health_report as hr
from prompt_load import _tools
from r2py.harness.objective import entity_score
from r2py.stage4.decompose import _compare_entity_bundles
from r2py.types import EffectClass

STEMS = sys.argv[1:] or ["prodlim__rd_example__backGround_Rd", "recipes__rd_example__step_kpca_Rd",
    "shape__rd_example__filledmultigonal_Rd", "shape__rd_example__getellipse_Rd", "isoband__vignette__isoband3_s2",
    "shape__rd_example__Arrows_Rd", "e1071__rd_example__boxplot_bclust_Rd"]
rd, pol = ROOT / "work/dsflash_default", "default_2026_11_01_dsflash"

def summ(fp):
    if fp is None: return None
    out = {}
    for k, v in fp.items():
        if isinstance(v, list) and v and isinstance(v[0], (int, float)):
            out[k] = f"n={len(v)} [{min(v):.3g},{max(v):.3g}]"
        elif isinstance(v, list):
            out[k] = v[:8]
        else:
            out[k] = v
    return out

def dump(stem):
    start = (hr.SOURCES / f"{stem}.py").read_text(encoding="utf-8")
    sm = pickle.loads((hr.MAPS / f"{stem}.pkl").read_bytes())
    tf = rd / "trajectories" / f"{stem}.{pol}.0.jsonl"
    recs = [json.loads(l) for l in open(tf, encoding="utf-8")] if tf.exists() else []
    src = hr._final_program(recs) or start
    t = _tools(sm, stem); t.note_reference(start)
    rep = t.verify(src)
    rb, pb = sm.entity_bundles or {}, rep.py_entity_bundles or {}
    print(f"=== {stem} aggregate {rep.aggregate:.3f}")
    for e, es in rep.by_entity.items():
        if e not in rb or e not in pb: continue
        r_eb, p_eb = rb[e], pb[e]
        res = _compare_entity_bundles(r_eb, p_eb).get(EffectClass.GRAPHICS)
        if res is None or res.score >= 0.99: continue
        rg = r_eb.graphics if isinstance(r_eb.graphics, int) else len(r_eb.graphics or [])
        pg = p_eb.graphics if isinstance(p_eb.graphics, int) else len(p_eb.graphics or [])
        print(f"-- {e} entity {entity_score(es):.3f} graphics {res.score:.3f}: {res.explanation}  pages R={rg} Py={pg}")
        for i, fp in enumerate(r_eb.graphics_meta or []): print(f"   R  p{i}: {summ(fp)}")
        for i, fp in enumerate(p_eb.graphics_meta or []): print(f"   Py p{i}: {summ(fp)}")
    return sm, src

if __name__ == "__main__":
    for s in STEMS:
        try: dump(s)
        except Exception as ex: print("ERR", s, ex)

"""Epoch 15 check (2026-11-16): per-entity R and Python page fingerprints of the reference programs that moved."""
import json, pickle, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(ROOT / "work/analysis")]
from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=True)
import health_report as hr
from prompt_load import _tools
from r2py.harness.objective import entity_score
from r2py.stage4.decompose import _compare_entity_bundles
from r2py.types import EffectClass
from graphics_meta_dump import summ

ref = {r["id"]: r for r in json.loads((ROOT / "work/scoring/reference.json").read_text())}
for pid in sys.argv[1:]:
    it = ref[pid]; stem = Path(it["script"]).stem
    sm = pickle.loads((hr.MAPS / f"{stem}.pkl").read_bytes())
    t = _tools(sm, stem); t.note_reference((hr.SOURCES / f"{stem}.py").read_text(encoding="utf-8"))
    rep = t.verify((ROOT / it["file"]).read_text(encoding="utf-8"))
    rb, pb = sm.entity_bundles or {}, rep.py_entity_bundles or {}
    print(f"=== {pid} {rep.aggregate:.3f}")
    for e, es in rep.by_entity.items():
        if e not in rb or e not in pb: continue
        r_eb, p_eb = rb[e], pb[e]
        if not (r_eb.graphics_meta or p_eb.graphics_meta or r_eb.graphics or p_eb.graphics): continue
        res = _compare_entity_bundles(r_eb, p_eb).get(EffectClass.GRAPHICS)
        print(f"-- {e} entity {entity_score(es):.3f} graphics {res.score:.3f} {res.explanation or ''}")
        for i, fp in enumerate(r_eb.graphics_meta or []): print(f"   R  p{i}: {summ(fp)}")
        for i, fp in enumerate(p_eb.graphics_meta or []): print(f"   Py p{i}: {summ(fp)}")

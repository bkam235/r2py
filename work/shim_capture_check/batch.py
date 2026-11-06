import sys, json, pickle, re, glob
from pathlib import Path
ROOT = Path(r"C:\Users\bened\Desktop\r2py_v0.3")
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=True)
import health_report as hr
from prompt_load import _tools
from r2py.harness.objective import entity_score
MAPS, SRC = hr.MAPS, hr.SOURCES
out = open(sys.argv[1], "w", encoding="utf-8")
for pool, rd, pol in (("training", "work/replay_default_e8", "default_2026_11_01"),
                      ("heldout", "work/refuse_done_heldout", "default_2026_11_01_rd")):
    stems = sorted({Path(json.loads(l)["script"]).stem for l in open(ROOT / rd / "results.jsonl", encoding="utf-8")})
    for stem in stems:
        start = (SRC / f"{stem}.py").read_text(encoding="utf-8")
        m = re.search(r"for _r2py_shim_n in (\[.*?\])", start)
        shim = set(eval(m.group(1))) if m else set()
        if not shim: continue
        sm = pickle.loads((MAPS / f"{stem}.pkl").read_bytes())
        aff = {e: sorted(set(b.data or {}) & shim) for e, b in (sm.entity_bundles or {}).items()}
        aff = {e: k for e, k in aff.items() if k}
        if not aff: continue
        tf = ROOT / rd / "trajectories" / f"{stem}.{pol}.0.jsonl"
        recs = [json.loads(l) for l in open(tf, encoding="utf-8")] if tf.exists() else []
        src = hr._final_program(recs) or start
        try:
            t = _tools(sm, stem); t.note_reference(start)
            rep = t.verify(src)
        except Exception as ex:
            out.write(json.dumps(dict(pool=pool, stem=stem, error=str(ex)[:200])) + "\n"); out.flush(); continue
        n = sum(1 for es in rep.by_entity.values() if es.active_dims) or 1
        pb = getattr(rep, "py_entity_bundles", {}) or {}
        ents = {}
        for e, keys in aff.items():
            es = rep.by_entity.get(e)
            ents[e] = dict(keys=keys, score=round(entity_score(es), 3) if es else None,
                           py_keys=sorted((pb[e].data or {}).keys()) if e in pb and pb[e] else None,
                           data=getattr(es, "data_output", None) if es else None)
        bound = sum(1 - v["score"] for v in ents.values() if v["score"] is not None) / n
        out.write(json.dumps(dict(pool=pool, stem=stem, aggregate=round(rep.aggregate, 4), n=n, ents=ents,
                                  bound=round(bound, 4))) + "\n"); out.flush()
        print(pool, stem, round(rep.aggregate, 3), {e: v["score"] for e, v in ents.items()}, flush=True)

"""Full feedback messages of chosen entities of a default final (offline)."""
import json, pickle, sys, glob
from pathlib import Path
ROOT = Path(r"C:\Users\bened\Desktop\r2py_v0.3"); sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=True)
import health_report as hr
from prompt_load import _tools
stem, ents = sys.argv[1], sys.argv[2:]
start = (hr.SOURCES / f"{stem}.py").read_text(encoding="utf-8")
sm = pickle.loads((hr.MAPS / f"{stem}.pkl").read_bytes())
f = glob.glob(str(ROOT / f"work/dsflash_default/trajectories/{stem}.*"))[0]
src = hr._final_program([json.loads(l) for l in open(f, encoding="utf-8")]) or start
t = _tools(sm, stem); t.note_reference(start); rep = t.verify(src)
for fb in rep.feedback:
    if fb.entity_id in ents and "tempfile:" not in fb.message[:20]:
        print(f"--- {fb.entity_id} {fb.effect_class} {fb.score:.3f}\n{fb.message[:1500]}")
for e in ents:
    es = rep.by_entity.get(e)
    if es: print(e, {d: round(getattr(es, d), 3) for d in es.active_dims})

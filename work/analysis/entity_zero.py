"""Entities of a default final that score 0 on data with no feedback of their own: what R holds, what Python recorded."""
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
for e in ents:
    es = rep.by_entity.get(e)
    print("=====", e)
    print(" R entity bundle:", str((sm.entity_bundles or {}).get(e))[:600])
    print(" R type:", (sm.entity_types or {}).get(e))
    print(" py entity score attrs:", {k: str(v)[:300] for k, v in vars(es).items()} if es else None)
lines = [l for l in src.splitlines() if any(f"# r2py:entity {e}" in l or f"'{e}'" in l or f'"{e}"' in l for e in ents)]
print("\n".join(lines[:20]))

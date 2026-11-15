"""Q3 (2026-11-15): do R's random temp-file names (FILES key 'tempfile:<basename>') reach the score?
Verify each default final as stored, and with every 'tempfile:*' entry removed from the map's R bundles. Offline."""
import json, pickle, sys, glob, copy
from pathlib import Path
ROOT = Path(r"C:\Users\bened\Desktop\r2py_v0.3"); sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=True)
import health_report as hr
from prompt_load import _tools
from r2py.harness.objective import entity_score

def strip(sm):
    sm = copy.deepcopy(sm); n = 0
    for holder in list(sm.entities.values()) + list(sm.effects):
        b = getattr(holder, "actual_bundle", None)
        if b is not None and getattr(b, "files", None):
            keep = {k: v for k, v in b.files.items() if not k.startswith("tempfile:")}
            n += len(b.files) - len(keep); b.files = keep
    return sm, n

for stem in sys.argv[1:]:
    start = (hr.SOURCES / f"{stem}.py").read_text(encoding="utf-8")
    sm0 = pickle.loads((hr.MAPS / f"{stem}.pkl").read_bytes())
    f = glob.glob(str(ROOT / f"work/dsflash_default/trajectories/{stem}.*"))[0]
    src = hr._final_program([json.loads(l) for l in open(f, encoding="utf-8")]) or start
    sm1, n = strip(sm0)
    for name, sm in (("stored", sm0), (f"no tempfile keys ({n} removed)", sm1)):
        t = _tools(sm, stem); t.note_reference(start); rep = t.verify(src)
        low = {e: round(entity_score(es), 3) for e, es in rep.by_entity.items() if es.active_dims and entity_score(es) < 0.999}
        print(f"{stem[:42]:42s} {name:28s} {rep.aggregate:.4f} exit {rep.py_exit_code} below1 {low}", flush=True)

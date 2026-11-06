import sys, pickle
from pathlib import Path
ROOT = Path(r"C:\Users\bened\Desktop\r2py_v0.3")
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=True)
import health_report as hr
from prompt_load import _tools
from r2py.harness.objective import entity_score
stem, path, ent = sys.argv[1], sys.argv[2], sys.argv[3]
sm = pickle.loads((hr.MAPS / f"{stem}.pkl").read_bytes())
t = _tools(sm, stem); t.note_reference((hr.SOURCES / f"{stem}.py").read_text(encoding="utf-8"))
src = Path(path).read_text(encoding="utf-8")
for i, (old, new) in enumerate([(None, None)] + [tuple(x.split("=>")) for x in sys.argv[4:]]):
    s = src if old is None else src.replace(old.replace("\n", "\n"), new.replace("\n", "\n"))
    assert old is None or s != src, f"variant {i}: pattern not found"
    rep = t.verify(s)
    pb = getattr(rep, "py_entity_bundles", {}) or {}
    print(f"variant {i}: aggregate {rep.aggregate:.4f}; {ent} {entity_score(rep.by_entity[ent]):.3f}; py data keys {list((pb.get(ent).data if pb.get(ent) else {}).keys())}")

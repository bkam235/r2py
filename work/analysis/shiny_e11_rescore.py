"""Shiny updateRadioButtons under epoch 11 (2026-11-14, offline): every rewrite a DeepSeek Flash chain logged on the
state, re-scored with the current scorer against the frozen start; per chain, the logged best and the epoch-11 best,
and how many candidates rebind the `ui` module name."""
import glob, json, pickle, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=True)
import health_report as hr
from prompt_load import _tools
stem = "shiny__rd_example__updateRadioButtons_Rd"
start = (hr.SOURCES / f"{stem}.py").read_text(encoding="utf-8")
sm = pickle.loads((hr.MAPS / f"{stem}.pkl").read_bytes())
files = (glob.glob(str(ROOT / f"work/dsflash_default/trajectories/{stem}.*")) +
         glob.glob(str(ROOT / f"work/feedback_e10/trajectories/{stem}.*")) +
         glob.glob(str(ROOT / f"work/patience_dsflash/trajectories/{stem}.*")) +
         glob.glob(str(ROOT / f"work/model_screen/trajectories/{stem}.stall2_ps_dsflash.*")) +
         glob.glob(str(ROOT / f"work/probe_crossover/trajectories/{stem}.px_ds_ds.*")))
cache = {}
def score(src):
    if src not in cache:
        t = _tools(sm, stem); t.note_reference(start); cache[src] = t.verify(src).aggregate
    return cache[src]
rows = []
for f in files:
    chains = {}
    for l in open(f, encoding="utf-8"):
        r = json.loads(l)
        if r["kind"] == "step" and r["outcome"].startswith("rewrite") and r.get("source"):
            chains.setdefault(r.get("branch"), []).append(r)
    for b, rs in chains.items():
        logged = max([r.get("aggregate") or 0 for r in rs])
        e11 = [round(score(r["source"]), 3) for r in rs]
        rebind = sum(bool(re.search(r"^ui\s*=\s*ui\.", r["source"], re.M)) for r in rs)
        rows.append((Path(f).parent.parent.name, Path(f).name.split(stem + ".")[1][:40], b, len(rs), logged, e11, rebind))
        print(rows[-1], flush=True)
n = len(rows)
print(f"chains {n}; logged best >= 0.9: {sum(r[4] >= 0.9 for r in rows)}; epoch-11 best >= 0.9: {sum(max(r[5]) >= 0.9 for r in rows)}; "
      f"first rewrite >= 0.9 under epoch 11: {sum(r[5][0] >= 0.9 for r in rows)}; candidates {sum(r[3] for r in rows)}, rebinding ui {sum(r[6] for r in rows)}")

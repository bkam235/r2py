"""Trace the score difference between the offline re-verification and the replay harness (2026-11-13).

Verifies one recorded chain-best program four ways: {prompt_load._tools, replay-style HarnessTools} x {with,
without ho.pinned_llm}, and prints the aggregate, per-entity scores and feedback of each.

    python work/patience_dsflash/trace_paths.py farver__rd_example__convert_colour_Rd.R 1
"""
import contextlib, sys, tempfile, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=True)
import replay, patience_continue as p
from prompt_load import _tools
from r2py import heldout as ho
from r2py.harness.tools import HarnessTools
from r2py.library import PatternLibrary
from r2py.harness.objective import entity_score

script, b = sys.argv[1], int(sys.argv[2])
stem = Path(script).stem
manifest = ho.load_manifest(ROOT / "experiments/dev_run/manifest.json"); cfg = manifest["protocol"]["translate"]
src = p.chains()[(script, b)]["source"]
sm = replay._script_map(script, manifest, replay.TRAIN_MAPS)
tmp = tempfile.mkdtemp()
shutil.copytree(ROOT / "work/dev_run/checkpoints/empty", Path(tmp) / "lib")
builders = {
    "tools": lambda: _tools(sm, stem),
    "replay": lambda: HarnessTools(sm, PatternLibrary(Path(tmp) / "lib"), model=cfg["model"],
                                   data_compare=cfg["data_compare"], timeout_s=cfg["timeout_s"],
                                   sidecar_filename=f"{stem}.r2py_data.json", runtime=None),
}
for name, build in builders.items():
    for pinned in (False, True):
        ctx = ho.pinned_llm(cfg["model"], ho.llm_settings(manifest)) if pinned else contextlib.nullcontext()
        with ctx:
            h = build(); h.note_reference(src)
            rep = h.verify(src)
        ents = {e: round(entity_score(es), 3) for e, es in rep.by_entity.items() if es.active_dims}
        print(f"== {name:6s} pinned={pinned}: aggregate {rep.aggregate:.4f} exit {rep.py_exit_code}  {ents}", flush=True)
        for f in (getattr(rep, "feedback", None) or [])[:6]:
            print(f"     {f.entity_id}: {f.message[:220]}", flush=True)

"""Verify chain-best programs the way replay.run_one does (no agent, no model calls except entity mapping)."""
import sys, tempfile, shutil
from pathlib import Path
ROOT = Path(r"C:/Users/bened/Desktop/r2py_v0.3")
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=True)
import replay, patience_continue as p
from r2py import heldout as ho
from r2py.harness.tools import HarnessTools
from r2py.library import PatternLibrary
manifest = ho.load_manifest(ROOT / "experiments/dev_run/manifest.json"); cfg = manifest["protocol"]["translate"]
ch = p.chains(); states = replay.training_states()
for script, b in [("farver__rd_example__convert_colour_Rd.R", 1), ("caret__vignette__caret_s3.R", 2), ("recipes__rd_example__step_kpca_Rd.R", 0)]:
    with ho.pinned_llm(cfg["model"], ho.llm_settings(manifest)), tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        sm = replay._script_map(script, manifest, replay.TRAIN_MAPS)
        shutil.copytree(ROOT / "work/dev_run/checkpoints/empty", Path(tmp) / "lib")
        h = HarnessTools(sm, PatternLibrary(Path(tmp) / "lib"), model=cfg["model"], data_compare=cfg["data_compare"],
                         timeout_s=cfg["timeout_s"], sidecar_filename=f"{Path(script).stem}.r2py_data.json", runtime=None)
        src = ch[(script, b)]["source"]
        out = []
        for ref in ("chain", "start"):
            h.note_reference(src if ref == "chain" else states[script]["source"])
            out.append((ref, round(h.verify(src).aggregate, 4)))
        print(f"{script[:40]:40s} b{b} recorded {ch[(script, b)]['best']:.4f} replay path {out}", flush=True)

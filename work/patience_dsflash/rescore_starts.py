"""Re-verify, 3 times each, the recorded chain-best programs whose continuation started at another score."""
import json, pickle, sys
from pathlib import Path
ROOT = Path(r"C:/Users/bened/Desktop/r2py_v0.3")
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=True)
import health_report as hr
from prompt_load import _tools
import patience_continue as p
ch = p.chains()
cases = [("farver__rd_example__convert_colour_Rd.R", 1), ("caret__vignette__caret_s3.R", 2),
         ("openssl__rd_example__ec_dh_Rd.R", 1), ("recipes__rd_example__step_kpca_Rd.R", 0),
         ("shape__rd_example__Arrows_Rd.R", 0)]
for script, b in cases:
    stem = Path(script).stem
    sm = pickle.loads((hr.MAPS / f"{stem}.pkl").read_bytes())
    start = (hr.SOURCES / f"{stem}.py").read_text(encoding="utf-8")
    src = ch[(script, b)]["source"]
    scores = []
    for _ in range(3):
        t = _tools(sm, stem); t.note_reference(start)
        rep = t.verify(src)
        scores.append(round(rep.aggregate, 4))
    print(f"{stem[:42]:42s} b{b} recorded {ch[(script, b)]['best']:.4f} re-verified {scores}", flush=True)

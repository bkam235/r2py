"""module-rebind follow-up (2026-11-14): lubridate period (baseline run 0 errored) and openssl ec_dh repeats."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
import scoring_epoch as se
base = json.load(open(ROOT / "work/scoring/baseline.json", encoding="utf-8"))
ref = {r["id"]: r for r in json.load(open(ROOT / "work/scoring/reference.json", encoding="utf-8"))}
for pid, n in [("final_default:lubridate__rd_example__period_Rd", 1),
               ("start:openssl__rd_example__ec_dh_Rd", 4), ("final_default:openssl__rd_example__ec_dh_Rd", 4)]:
    b = [r.get("aggregate") for r in base[pid]["runs"]]
    new = [se.verify_one(ref[pid]).get("aggregate") for _ in range(n)]
    print(pid, "baseline runs", b, "new", new)

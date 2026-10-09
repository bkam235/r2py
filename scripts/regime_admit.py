"""Admit a near-miss runtime function for the option values it is verified on, and make it loud elsewhere.

Rd-harvested cases are the documented edge cases, so a function can be right everywhere except one
documented option: `time_add` reproduces R on every call except non-default `roll_dst`, whose rule
lives in timechange's C++ and is never shown to the model. All-core-cases acceptance throws such a
function away. This keeps it, fenced:

* the function's final code is re-run on its Rd-harvested cases (deterministic; no model calls);
* a failing case is *fenceable* only if it passes an explicit option value - a character-valued
  keyword argument like `roll_dst = "pre"`; every such value seen in a failing call is fenced, even
  if it passes on other inputs. Numeric amounts (`hour = 1`) are inputs, not regimes, and are never
  fenced. Failures with no such value (wrong vectorisation,
  a plain value error) are bugs, not regimes, and block admission;
* the fence covers values passed explicitly; a call that leaves the option at its default runs
  the implementation, and is only as verified as the default-regime cases are;
* the pilot's failure record must be complete (records from before 2026-10-08 kept only five);
* every failure the pilot itself recorded (it also ran the model's invented calls) must be covered
  by the fence - a known failure outside it would ship a silently wrong function;
* the guarded function must reproduce R on every remaining case (at least three), and must raise
  on every fenced one.

The admitted entry has status `passed_restricted` and records the fenced values, which the runtime
store passes on to the translator.

    python scripts/regime_admit.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

PILOT = ROOT / "work" / "runtime" / "rd_pilot"
OUT = ROOT / "work" / "runtime" / "rd_restricted"     # admitted copies; the pilot records stay as they were
HARVEST = ROOT / "work" / "rd_harvest" / "rows.jsonl"
from r2py.runtime.admit import MIN_IN_REGIME, _GUARD, _numeric, _scalar, assess, guarded  # noqa: E402,F401


def main() -> int:
    from rd_pilot import as_mined

    harvested = {(r["function"], r["package"]): r for r in map(json.loads, HARVEST.open(encoding="utf-8"))}
    admitted = 0
    for f in sorted(PILOT.glob("*.json")):
        rec = json.loads(f.read_text(encoding="utf-8"))
        if rec.get("status") != "failed" or not rec.get("code"):
            continue
        row = harvested.get((rec["function"], rec.get("package") or "base"))
        if not row:
            continue
        a = assess(rec, as_mined(row))
        print(f"{rec['function']:<16} {a['verdict']}")
        for k in ("n_cases", "failing", "fenced", "in_regime", "inside_passed", "outside_refused", "unfenceable"):
            if k in a:
                print(f"     {k:<16}{a[k]}")
        if a.get("code"):
            admitted += 1
            OUT.mkdir(parents=True, exist_ok=True)
            (OUT / f"{f.stem}.py").write_text(a["code"], encoding="utf-8")
            entry = dict(rec, status="passed_restricted", unverified=a["fenced"], code=a["code"],
                         restricted_evidence={"in_regime": a["inside_passed"], "refused": a["outside_refused"]})
            (OUT / f.name).write_text(json.dumps(entry, indent=1), encoding="utf-8")
    print(f"\nadmitted with restrictions: {admitted}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

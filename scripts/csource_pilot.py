"""Does showing the compiled source fix the functions whose R source is only a wrapper?

`time_add`, `time_subtract` and `time_update` failed the Rd pilot on their DST and month-end rolling
rules. Their R bodies are ~1,600-character wrappers ending in `.Call(_timechange_C_time_add)`: the
rules live in timechange's C++ (src/update.cpp, src/common.*), which the model never saw. Same
functions, same Rd-harvested cases, two arms:

  r_only    what the pilot did: R source, usage, cases
  with_cpp  the same plus the C++ routine the wrapper calls and the rolling helpers it uses

Every run records its complete failure list (propose keeps them all now), and each result is judged
by `regime_admit.assess`, so a near miss can still be admitted with its failing option values fenced.

The C++ comes from the CRAN source tarball of the installed version (work/csource/, extracted
`src/` only; read as text, never compiled or run).

    python scripts/csource_pilot.py --workers 6
    python scripts/csource_pilot.py --summary-only
"""
from __future__ import annotations

import argparse
import json
import multiprocessing
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

SRC = ROOT / "work" / "csource" / "timechange" / "src"
CIVIL_LOOKUP = ROOT / "work" / "csource" / "cctz_civil_lookup.h"   # the struct and its comments, cut from cctz/time_zone.h
OUT = ROOT / "work" / "runtime" / "csource"
HARVEST = ROOT / "work" / "rd_harvest" / "rows.jsonl"
ARMS = ("r_only", "with_cpp")
# function -> the C++ routine its R wrapper reaches (time_subtract negates and calls time_add)
ROUTINE = {"time_add": "C_time_add", "time_subtract": "C_time_add", "time_update": "C_time_update"}


def routine_source(name: str) -> str:
    """One top-level C++ function from update.cpp, by its name: its signature through the closing
    brace in column 0 (every top-level function in that file ends that way)."""
    lines = (SRC / "update.cpp").read_text(encoding="utf-8").splitlines()
    start = next(i for i, l in enumerate(lines) if f" {name}(" in l and not l.startswith(" "))
    while start > 0 and lines[start - 1].strip().startswith("[[cpp11"):
        start -= 1
    end = next(i for i in range(start + 1, len(lines)) if lines[i] == "}")
    return "\n".join(lines[start:end + 1])


def cpp_hint(fname: str) -> str:
    common = (SRC / "common.h").read_text(encoding="utf-8") + "\n" + (SRC / "common.cpp").read_text(encoding="utf-8")
    return ("The R function above is a thin wrapper: its behaviour, including every `roll_month` and `roll_dst` "
            "rule, is implemented in C++ in the timechange package. This is that C++, from the package source "
            "(timechange 0.4.0). Reproduce its rules exactly; where the R wrapper and the C++ disagree, the C++ "
            "decides what R returns.\n\n"
            f"```cpp\n// src/update.cpp: the routine the wrapper calls\n{routine_source(ROUTINE[fname])}\n```\n\n"
            f"```cpp\n// src/common.h and src/common.cpp: the rolling helpers it uses\n{common}\n```\n\n"
            "The DST resolution uses cctz's `civil_lookup` (Google cctz, the time-zone library timechange "
            "vendors); in Python, `zoneinfo` resolves the same gaps and overlaps through `fold`:\n"
            f"```cpp\n// src/cctz/time_zone.h\n{CIVIL_LOOKUP.read_text(encoding='utf-8')}\n```")


def task(args: tuple) -> dict:
    fname, arm, mined = args
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    from r2py import heldout as ho
    from r2py.runtime import propose

    man = ho.load_manifest(str(ROOT / "experiments/dev_run/manifest.json"))
    cfg = man["protocol"]["translate"]
    hint = cpp_hint(fname) if arm == "with_cpp" else ""
    with ho.pinned_llm(cfg["model"], ho.llm_settings(man)):
        rec = propose.attempt(fname, "timechange", cfg["model"], rounds=8, attempts=4, mined=mined,
                              source_limit=15000, budget_s=1800, locate=True, hint=hint)
    rec.update(tag=f"csource {arm}", arm=arm, n_rd_cases=len(mined), hint_chars=len(hint))
    propose.save(rec, OUT / arm)
    return rec


def judged(rec: dict, mined: list[dict]) -> str:
    import regime_admit
    if rec.get("status") == "passed":
        return "passed outright"
    return regime_admit.assess(rec, mined)["verdict"]


def summarise(rows: list[dict], cases: dict) -> str:
    lines = [f"{'function':<15}{'arm':<10}{'status':<9}{'core':>8}{'fails':>7}{'rounds':>7}  verdict"]
    for r in sorted(rows, key=lambda r: (r["function"], r.get("arm", ""))):
        lines.append(f"{r['function']:<15}{r.get('arm', '?'):<10}{r.get('status', '?'):<9}"
                     f"{str(r.get('core_passed')) + '/' + str(r.get('core_total')):>8}"
                     f"{r.get('n_failures', len(r.get('failures') or [])):>7}{r.get('rounds', '-'):>7}  "
                     f"{judged(r, cases[r['function']])}")
    return "\n".join(lines)


def main() -> int:
    from r2py.keepawake import keep_awake
    from rd_pilot import as_mined
    keep_awake()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--summary-only", action="store_true")
    ap.add_argument("--show-hint", default=None, help="print the C++ hint for one function and exit")
    args = ap.parse_args()
    if args.show_hint:
        print(cpp_hint(args.show_hint))
        return 0

    harvested = {r["function"]: r for r in map(json.loads, HARVEST.open(encoding="utf-8"))
                 if r["package"] == "timechange"}
    cases = {f: as_mined(harvested[f]) for f in ROUTINE}
    if args.summary_only:
        rows = [json.loads(f.read_text(encoding="utf-8")) for arm in ARMS for f in sorted((OUT / arm).glob("*.json"))]
        print(summarise(rows, cases))
        return 0
    tasks = [(f, arm, cases[f]) for f in ROUTINE for arm in ARMS
             if not (OUT / arm / f"timechange__{f}.json").exists()]
    print(f"{len(tasks)} runs: " + ", ".join(f"{f}/{a}" for f, a, _ in tasks), flush=True)
    ctx = multiprocessing.get_context("spawn")
    rows = []
    with ctx.Pool(args.workers) as pool:
        for rec in pool.imap_unordered(task, tasks):
            rows.append(rec)
            print(f"   {rec['function']:<15}{rec['arm']:<10}{rec.get('status', '?'):<9}"
                  f"core {rec.get('core_passed')}/{rec.get('core_total')}  rounds {rec.get('rounds')}", flush=True)
    print("\n" + summarise(rows, cases))
    return 0


if __name__ == "__main__":
    sys.exit(main())

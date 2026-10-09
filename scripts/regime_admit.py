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
MIN_IN_REGIME = 3

_GUARD = '''

_R2PY_UNVERIFIED_{FUNC} = {FENCED}


def {FUNC}(*args, **kwargs):
    """{FUNC} reproduces R on every tested call except the option values listed in
    _R2PY_UNVERIFIED_{FUNC}; for those it refuses rather than guess."""
    import inspect
    try:
        bound = inspect.signature(_r2py_impl_{FUNC}).bind(*args, **kwargs).arguments
    except TypeError:
        bound = kwargs
    for name, bad in _R2PY_UNVERIFIED_{FUNC}.items():
        v = bound.get(name)
        if isinstance(v, (list, tuple)) and len(v) == 1:
            v = v[0]
        if v is not None and str(v) in bad:
            raise NotImplementedError(
                f"{FUNC}: {{name}}={{v!r}} is not verified against R; handle this case in your own code")
    return _r2py_impl_{FUNC}(*args, **kwargs)
'''


def _scalar(v):
    """The option value of a serialised argument, or None if it is not a scalar option."""
    if isinstance(v, list) and len(v) == 1:
        v = v[0]
    if isinstance(v, (str, int, float, bool)):
        return str(v)
    return None


def _numeric(v) -> bool:
    if isinstance(v, list) and len(v) == 1:
        v = v[0]
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def guarded(code: str, func: str, fenced: dict[str, set[str]]) -> str:
    """The model's implementation renamed, behind a wrapper that refuses the fenced option values."""
    import re
    impl = re.sub(rf"\bdef {re.escape(func)}\(", f"def _r2py_impl_{func}(", code, count=1)
    impl = re.sub(rf"(?<![\w.]){re.escape(func)}\(", f"_r2py_impl_{func}(", impl)   # its own recursive calls
    impl = impl.replace(f"def _r2py_impl__r2py_impl_{func}(", f"def _r2py_impl_{func}(")
    table = "{" + ", ".join(f"{k!r}: {sorted(v)!r}" for k, v in sorted(fenced.items())) + "}"
    return impl.rstrip() + "\n" + _GUARD.replace("{FUNC}", func).replace("{FENCED}", table)


def assess(rec: dict, cases: list[dict]) -> dict:
    from r2py.runtime import difftest

    fname = rec["function"]
    func = "r_" + difftest.py_name(fname)
    out = {"function": fname, "package": rec.get("package"), "n_cases": len(cases)}
    # Records written before propose kept every failure hold only the first five: an admission
    # judged on five of sixteen failures is not a judgement.
    n_failed = rec.get("n_failures", (rec.get("core_total") or 0) - (rec.get("core_passed") or 0))
    if len(rec.get("failures") or []) < n_failed:
        out["verdict"] = (f"not admissible: failure record incomplete ({len(rec.get('failures') or [])} of "
                          f"{n_failed} recorded) - re-run the attempt")
        return out
    res = difftest.run_python(rec["code"], fname, cases)
    failed_calls = {f["call"] for f in res.failures}
    failing = [c for c in cases if c["call"] in failed_calls]
    out["failing"] = len(failing)
    if not failing:
        # Right on every documented case, wrong on cases the pilot added (vector input, NA, ...):
        # with no option value to fence, those failures are a bug.
        out["verdict"] = ("not admissible: passes every Rd case, fails the pilot's other cases (a bug, not a regime)"
                          if n_failed else "passes every case")
        return out
    # Fence only *option* values: character-valued keyword arguments (enums such as roll_dst = "pre").
    # Numeric amounts (hour = 1, month = 2) are inputs, not regimes - fencing them would refuse every
    # February. An option value that fails on some inputs and passes on others is still unverified:
    # time_add is right with roll_dst = "pre" until the call crosses a DST boundary.
    def options(c):
        return {(name, _scalar(val)) for name, val in c["args"]
                if name and _scalar(val) is not None and not _numeric(val)}

    fenced: dict[str, set[str]] = {}
    unfenceable = []
    for c in failing:
        culprits = options(c)
        if not culprits:
            unfenceable.append(c["call"])
            continue
        for name, val in culprits:
            fenced.setdefault(name, set()).add(val)
    if unfenceable:
        out["verdict"] = "not admissible: failures with no option value (a bug, not a regime)"
        out["unfenceable"] = unfenceable[:4]
        return out

    # The pilot run saw more cases than the Rd harvest (the model's own example calls), and recorded
    # their failures. A known failure the fence does not cover would ship a silently wrong function:
    # time_subtract returns one value where R returns three, on vector input the Rd cases never use.
    import re as _re
    uncovered = [f["call"].split("   [")[0] for f in rec.get("failures") or []
                 if not any(_re.search(rf'\b{_re.escape(n)}\s*=\s*"{_re.escape(v)}"', f["call"])
                            for n, vals in fenced.items() for v in vals)]
    if uncovered:
        out["fenced"] = {k: sorted(v) for k, v in fenced.items()}
        out["verdict"] = "not admissible: recorded failures outside the fence (a bug, not a regime)"
        out["unfenceable"] = uncovered[:4]
        return out

    def hit(c):
        return any(name in fenced and _scalar(val) in fenced[name] for name, val in c["args"] if name)

    inside = [c for c in cases if not hit(c)]
    outside = [c for c in cases if hit(c)]
    out["fenced"] = {k: sorted(v) for k, v in fenced.items()}
    out["in_regime"], out["out_of_regime"] = len(inside), len(outside)
    if len(inside) < MIN_IN_REGIME:
        out["verdict"] = f"not admissible: only {len(inside)} cases left inside the verified regime"
        return out
    code = guarded(rec["code"], func, fenced)
    ok_inside = difftest.run_python(code, fname, inside)
    refused = difftest.run_python(code, fname, outside)
    loud = sum(1 for f in refused.failures if "not verified against R" in str(f.get("error", "")))
    out["inside_passed"] = f"{ok_inside.passed}/{ok_inside.total}"
    out["outside_refused"] = f"{loud}/{len(outside)}"
    if ok_inside.passed == ok_inside.total and loud == len(outside):
        out["verdict"] = "admitted, restricted"
        out["code"] = code
    else:
        out["verdict"] = "not admissible: the guarded function does not behave as required"
    return out


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

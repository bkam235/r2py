"""The small model proposes Python implementations of R functions; R is the judge (roadmap step 7).

Per function: (1) the model lists example calls from its own knowledge of R; the harness runs them in R and mutates their
first argument, which gives differential test cases with R's answers (``difftest``); (2) the model writes
``def r_<name>(...)`` given R's usage and source and a few cases; (3) every failing case -- the call, what R returns, what
the Python returned or raised -- goes back for a corrected version, up to ``ROUNDS`` times.  A function is accepted only
when all cases pass.  Nothing is written by hand: the cases come from R, the verdict from comparison with R.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from ..stage2 import llm as _llm
from . import difftest

ROUNDS = 5          # counterexample rounds per attempt
ATTEMPTS = 3        # independent attempts (fresh conversations) per function
SOURCE_LIMIT = 6000

_CALLS_SYSTEM = "You know R well. Reply with R code only, one call per line, no commentary."

_IMPL_SYSTEM = (
    "You write Python functions that reproduce R functions exactly, including defaults, NA handling, ties, 1-based "
    "versus 0-based conventions, rounding and the type and shape of the result. Rules: the function is named "
    "`r_<name>` with dots in the R name replaced by underscores; its parameters have R's formal names (dots replaced by "
    "underscores) and R's defaults (R's `...` becomes `*args, **kwargs`); vectors arrive as numpy arrays (NA is NaN), strings as lists of str, data frames as "
    "pandas DataFrames; return a numpy array, scalar, list, dict or DataFrame holding the values R returns (names are "
    "not compared; a factor is a list of str). Return the natural Python object for the R value, not a serialised form: "
    "bytes for a raw vector, a datetime / pandas Timestamp for POSIXct, a datetime.date for Date, a timedelta for difftime, "
    "a number for a number, a list of str for character, a bool for logical; the harness serialises your return value the way "
    "it serialises R's, and code that uses your function needs the real object. If the R function draws random numbers (sample, runif, rnorm ...), call the "
    "numpy or random equivalents with the same counts and sizes: the test harness serves R's own draws to them, so what "
    "must match is how the draws are used (order, number, indexing). If an R parameter name is a Python builtin "
    "(list, dict, type, str, ...), keep the name but reach the builtin through `import builtins` inside the function. Use only numpy, pandas, scipy and the standard library. No printing. "
    "Reply with the complete Python code only.")


def _code(raw: str) -> str:
    m = re.search(r"```(?:python)?\n(.*?)```", raw, re.DOTALL)
    return (m.group(1) if m else raw).strip() + "\n"


def propose_calls(fname: str, package: str | None, usage: str, model: str) -> list[str]:
    qual = f"{package}::{fname}" if package else fname
    prompt = (f"Write 8 different R calls to `{qual}`, one per line. Use only literal values and simple constructors "
              "(c(), seq(), rep(), 1:10, letters, matrix(), data.frame()); no set.seed, no files, no assignments. Cover a typical "
              "call, named arguments, a non-default option, NA values, tied values, negative numbers and a length-one input.\n"
              f"Usage: {usage}")
    raw = _llm.call([{"role": "user", "content": prompt}], _CALLS_SYSTEM, model=model, max_tokens=1500)
    lines = [l.strip() for l in re.sub(r"```\w*", "", raw).splitlines()]
    return [l for l in lines if re.match(rf"^({re.escape(package)}::)?{re.escape(fname)}\(", l or "")][:10] if package else \
           [l for l in lines if re.match(rf"^{re.escape(fname)}\(", l or "")][:10]


def _describe(cases: list[dict], n: int = 4) -> str:
    out = []
    for c in cases[:n]:
        out.append(f"{c['call']}\n  -> R returns an object of class '{c.get('rclass', '?')}', printed: {c.get('shown', '')[:300]}")
    return "\n".join(out)


def _failures(res: difftest.Result, n: int = 3) -> str:
    out = []
    for f in sorted(res.failures, key=lambda f: not f.get("core", True))[:n]:        # ordinary-use failures first
        got = f.get("error") or ("Python returned " + json.dumps(f.get("got"))[:300])
        out.append(f"{f['call']}\n  R returns (class '{f.get('rclass', '?')}', as values) {json.dumps(f.get('expected'))[:300]}\n  yours: {got}")
    return "\n".join(out)


def attempt(fname: str, package: str | None, model: str, rounds: int = ROUNDS, attempts: int = ATTEMPTS) -> dict:
    """Try to build a verified Python implementation of one R function; returns a record (never raises).

    The cases are built once.  The model gets up to ``attempts`` independent tries (fresh conversations: the sampled
    code differs), each with up to ``rounds`` counterexample rounds; the first version that passes every ordinary-use
    case (``difftest.label_core``) is accepted.  Cases that exercise odd input classes are reported, not required.
    """
    rec: dict = {"function": fname, "package": package, "status": "error", "rounds": 0}
    try:
        probe = difftest.build_cases(fname, [f"{fname}(1:5)"], package)            # usage and source need no model
        calls = propose_calls(fname, package, probe.get("usage", ""), model)
        built = difftest.build_cases(fname, calls, package)
        cases = built["cases"]
        core = [c for c in cases if c.get("core", True)]
        rec.update(n_calls=len(calls), n_cases=len(cases), n_core=len(core))
        if len(core) < 3:
            rec["status"] = "no_cases"                                              # R accepted fewer than three ordinary calls
            return rec
        base = (f"R function `{package + '::' if package else ''}{fname}`\nUsage: {built['usage']}\n"
                f"R source (may be a wrapper around compiled code):\n{built['source'][:SOURCE_LIMIT]}\n\n"
                f"Example calls with R's results:\n{_describe(core)}\n\n"
                f"Write `def r_{difftest.py_name(fname)}(...)`.")
        best = None
        for attempt_no in range(1, attempts + 1):
            messages = [{"role": "user", "content": base}]
            for rnd in range(1, rounds + 1):
                raw = _llm.call(messages, _IMPL_SYSTEM, model=model, max_tokens=6000)
                code = _code(raw)
                res = difftest.run_python(code, fname, cases)
                cur = dict(attempt=attempt_no, rounds=rnd, passed=res.passed, total=res.total, core_passed=res.core_passed,
                           core_total=res.core_total, code=code, failures=res.failures[:5])
                if best is None or (res.core_passed, res.passed) > (best["core_passed"], best["passed"]):
                    best = cur
                if res.ok_core:
                    rec.update(cur, status="passed", exotic_passed=res.passed - res.core_passed,
                               exotic_total=res.total - res.core_total)
                    return rec
                messages = [{"role": "user", "content": base},
                            {"role": "assistant", "content": raw},
                            {"role": "user", "content": f"{res.core_passed} of {res.core_total} ordinary cases pass. Failing cases:\n"
                                                        f"{_failures(res)}\nReturn the complete corrected code."}]
        rec.update(best, status="failed")
    except Exception as exc:
        rec["error"] = f"{type(exc).__name__}: {exc}"[:300]
    return rec


def save(rec: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{rec.get('package') or 'base'}__{rec['function']}"
    (out_dir / f"{stem}.json").write_text(json.dumps(rec, indent=1, default=str), encoding="utf-8")
    if rec.get("status") == "passed":
        (out_dir / f"{stem}.py").write_text(rec["code"], encoding="utf-8")

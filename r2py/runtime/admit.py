"""Admit a near-miss runtime function for the regime it is verified on, and make it loud elsewhere.

Moved from scripts/regime_admit.py (see its docstring for the rule and the three ways it went wrong
before it was right) so the harness can use it (the on-demand step, r2py/runtime/ondemand.py).
`assess(rec, cases)` returns a verdict and, when admitted, the guarded code. A regime is fenced by
option values (roll_dst = "pre") and, since 2026-10-09, by input classes of the first argument
(vector input, NA input) - the pilot's near misses were mostly vectorisation and NA failures.
"""
from __future__ import annotations

MIN_IN_REGIME = 3
VECTOR, NA = "vector input", "NA input"     # input classes a fence can refuse, besides option values

_GUARD = '''

_R2PY_UNVERIFIED_{FUNC} = {FENCED}
_R2PY_UNVERIFIED_CLASSES_{FUNC} = {CLASSES}


def _r2py_items_{FUNC}(v):
    if isinstance(v, (str, bytes, dict)) or not hasattr(v, "__len__"):
        return None
    try:
        return list(v)
    except TypeError:
        return None


def {FUNC}(*args, **kwargs):
    """{FUNC} reproduces R on every tested ordinary call except the option values in _R2PY_UNVERIFIED_{FUNC}
    and the input classes in _R2PY_UNVERIFIED_CLASSES_{FUNC}; for those it refuses rather than guess."""
    import inspect
    import math
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
                f"{FUNC}: {name}={v!r} is not verified against R; handle this case in your own code")
    if _R2PY_UNVERIFIED_CLASSES_{FUNC} and bound:
        first = next(iter(bound.values()))
        items = _r2py_items_{FUNC}(first)
        if "vector input" in _R2PY_UNVERIFIED_CLASSES_{FUNC} and items is not None and len(items) > 1:
            raise NotImplementedError(
                f"{FUNC}: input of length {len(items)} is not verified against R (verified for single values); "
                "loop over the elements or write this case yourself")
        vals = items if items is not None else [first]
        if "NA input" in _R2PY_UNVERIFIED_CLASSES_{FUNC} and any(
                x is None or (isinstance(x, float) and math.isnan(x)) for x in vals):
            raise NotImplementedError(f"{FUNC}: input containing NA is not verified against R; handle NA yourself")
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


_OPTION_WORD = None


def option_values(case: dict) -> set[tuple[str, str]]:
    """The option values a call passes: flags (logical) and enum keywords (short identifier-like strings such as
    "pre", "postday", "boundary"), never the first argument - that is the data the function works on.

    The first version fenced any character-valued keyword argument, and so fenced data: read_xml was "admitted"
    with x = '<!DOCTYPE doc ...>' fenced and encode_native with colour = 'grey10' - refusing those exact strings
    and staying silently wrong on every other input of the same kind (2026-10-09).
    """
    import re
    global _OPTION_WORD
    if _OPTION_WORD is None:
        _OPTION_WORD = re.compile(r"[A-Za-z_.][A-Za-z0-9_.\-]{0,23}")
    out = set()
    for i, (name, val) in enumerate(case.get("args") or []):
        if i == 0 or not name:
            continue
        raw = val[0] if isinstance(val, list) and len(val) == 1 else val
        if isinstance(raw, bool):
            out.add((name, str(raw)))
        elif isinstance(raw, str) and _OPTION_WORD.fullmatch(raw):
            out.add((name, raw))
    return out


def input_classes(case: dict) -> set[str]:
    """The input classes of a case's first argument, as the serialiser wrote it (R NA -> null)."""
    if not case.get("args"):
        return set()
    v = case["args"][0][1]
    out = set()
    if isinstance(v, list) and len(v) > 1:
        out.add(VECTOR)
    if v is None or (isinstance(v, list) and any(x is None for x in v)):
        out.add(NA)
    return out


def guarded(code: str, func: str, fenced: dict[str, set[str]], classes: set[str] | frozenset = frozenset()) -> str:
    """The model's implementation renamed, behind a wrapper that refuses the fenced option values and input classes."""
    import re
    impl = re.sub(rf"\bdef {re.escape(func)}\(", f"def _r2py_impl_{func}(", code, count=1)
    impl = re.sub(rf"(?<![\w.]){re.escape(func)}\(", f"_r2py_impl_{func}(", impl)   # its own recursive calls
    impl = impl.replace(f"def _r2py_impl__r2py_impl_{func}(", f"def _r2py_impl_{func}(")
    table = "{" + ", ".join(f"{k!r}: {sorted(v)!r}" for k, v in sorted(fenced.items())) + "}"
    return (impl.rstrip() + "\n" + _GUARD.replace("{FUNC}", func).replace("{FENCED}", table)
            .replace("{CLASSES}", repr(sorted(classes))))


def assess(rec: dict, cases: list[dict]) -> dict:
    """Admit ``rec`` for the regime it is verified on, if every ordinary-use failure can be fenced.

    Only *core* cases decide, exactly as for a plain pass: failures on odd input classes are reported, not
    required. A core failure is fenceable by an option value (a character-valued keyword argument such as
    roll_dst = "pre"; numeric amounts are inputs, never fenced) or, failing that, by the input class of its
    first argument (vector, NA). With the full case list ``propose`` used (``rec["cases"]``) every failure is
    judged directly; for older records every recorded failure must lie inside the option fence.
    """
    from r2py.runtime import difftest

    fname = rec["function"]
    func = "r_" + difftest.py_name(fname)
    out = {"function": fname, "package": rec.get("package"), "n_cases": len(cases)}
    # Records written before propose kept every failure hold only the first five: an admission
    # judged on five of sixteen failures is not a judgement.
    n_failed = rec.get("n_failures", (rec.get("core_total") or 0) - (rec.get("core_passed") or 0))
    if not rec.get("cases") and len(rec.get("failures") or []) < n_failed:
        out["verdict"] = (f"not admissible: failure record incomplete ({len(rec.get('failures') or [])} of "
                          f"{n_failed} recorded) - re-run the attempt")
        return out
    core = [c for c in cases if c.get("core", True)]
    res = difftest.run_python(rec["code"], fname, core)
    failed_calls = {f["call"] for f in res.failures}
    failing = [c for c in core if c["call"] in failed_calls]
    out["failing"] = len(failing)
    if not failing:
        out["verdict"] = ("not admissible: passes these cases, fails the attempt's other cases (a bug, not a regime)"
                          if n_failed and not rec.get("cases") else "passes every case")
        return out

    def options(c):
        return option_values(c)

    fenced: dict[str, set[str]] = {}
    classes: set[str] = set()
    unfenceable = []
    for c in failing:
        culprits = options(c)
        if culprits:
            for name, val in culprits:
                fenced.setdefault(name, set()).add(val)
            continue
        cls = input_classes(c)
        if cls:
            classes |= cls
            continue
        unfenceable.append(c["call"])
    if unfenceable:
        out["verdict"] = "not admissible: failures with no option value or input class to fence (a bug)"
        out["unfenceable"] = unfenceable[:4]
        return out

    if not rec.get("cases"):
        # Older records: the attempt saw cases we do not have; every recorded failure must be inside the fence.
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
        return (any(name in fenced and _scalar(val) in fenced[name] for name, val in c["args"] if name)
                or bool(input_classes(c) & classes))

    inside = [c for c in core if not hit(c)]
    outside = [c for c in core if hit(c)]
    out["fenced"] = {k: sorted(v) for k, v in fenced.items()}
    out["classes"] = sorted(classes)
    out["in_regime"], out["out_of_regime"] = len(inside), len(outside)
    if len(inside) < MIN_IN_REGIME:
        out["verdict"] = f"not admissible: only {len(inside)} cases left inside the verified regime"
        return out
    code = guarded(rec["code"], func, fenced, classes)
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

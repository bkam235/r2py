"""Compare objects JSON cannot represent, by value (Stage 4 Phase 1, generic: no per-class adapters).

Objects whose meaning is *numbers* (fitted models, ROC curves, distances): every number reachable on the Python
side forms a pool; each numeric field of the R object (a named vector of its captured value) counts as
reproduced if its values are found in the pool within tolerance, so labels, ordering and library layout do not
matter.  Objects whose meaning is *structure* (XML, rendered tags, date-times): the text forms are compared
after canonicalisation.  The numeric tier is chosen when the R object has informative numeric fields, the text
tier otherwise.

What counts as an informative field is calibrated, not guessed: ``scripts/fingerprint_null_report.py`` matches the
fields of one object against the numbers of unrelated objects over the whole corpus and reports the chance
match rate per field kind; the constants below are the ones that keep that rate under its target.
"""
from __future__ import annotations

import bisect
import math
import re
from typing import Any

from .base import _difflib_similarity

# Calibrated by scripts/fingerprint_null_report.py on the full-precision census of 2026-10-03 (309 scripts, 4000
# fields, 150 pools of 10 variables from other packages each): fields with >= 5 values of >= 5 significant digits
# match an unrelated object by chance at 0.0006; with 4 such values already at 0.02, and integer or low-precision
# fields at 0.6 (shared datasets, constants such as pi, 0/1 indicators).  Target: < 1e-3.
PRECISE_DIGITS = 5          # a value is distinctive with at least this many significant digits
MIN_PRECISE_VALUES = 5      # a field is informative with at least this many distinctive values
MATCH_FRACTION = 0.99       # share of a field's values that must be found in the pool
MAX_FIELD_WEIGHT = 20       # a long vector counts like this many values, not more

_XML_DECL_RE = re.compile(r"<\?xml[^>]*\?>")
_WS_RE = re.compile(r"\s+")
_GAP_RE = re.compile(r">\s+<")


def is_fp(v: Any) -> bool:
    return isinstance(v, dict) and v.get("__r2py_fp__") is True


def _is_num(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _as_vector(v: Any) -> list[float]:
    if _is_num(v):
        return [float(v)]
    if isinstance(v, list):
        return [float(x) for x in v if _is_num(x)]
    return []


def numeric_fields(value: Any) -> list[tuple[str, list[float]]]:
    """(path, values) for every numeric field of a plain value or fingerprint.

    A dict or list whose elements are all numbers is one field (a coefficient table, a residual vector); nested
    containers recurse.  Strings, booleans and nulls are not numeric.
    """
    if is_fp(value):
        nums = value.get("numbers") or {}
        if isinstance(nums, dict):
            return [(k, _as_vector(v)) for k, v in nums.items() if _as_vector(v)]
        vec = _as_vector(nums)
        return [("numbers", vec)] if vec else []
    out: list[tuple[str, list[float]]] = []

    def walk(v: Any, path: str) -> None:
        if _is_num(v):
            out.append((path, [float(v)]))
        elif isinstance(v, dict):
            items = list(v.items())
            if items and all(_is_num(x) for _, x in items):
                out.append((path, [float(x) for _, x in items]))
            else:
                for k, x in items:
                    walk(x, f"{path}.{k}" if path else str(k))
        elif isinstance(v, list):
            if v and all(_is_num(x) for x in v):
                out.append((path, [float(x) for x in v]))
            else:
                for i, x in enumerate(v):
                    walk(x, f"{path}[{i}]")
    walk(value, "")
    return out


def texts(value: Any) -> list[str]:
    if is_fp(value):
        t = value.get("texts", value.get("text"))
        return [t] if isinstance(t, str) else [x for x in (t or []) if isinstance(x, str)]
    return [value] if isinstance(value, str) else []


def significant_digits(v: float) -> int:
    """Significant digits of *v* at double precision, trailing zeros and float noise removed."""
    return len(("%.10g" % abs(v)).split("e")[0].replace(".", "").lstrip("0").rstrip("0"))


def informative(vals: list[float]) -> bool:
    """Could a match of this field be a coincidence?  Calibrated, see the constants above."""
    return sum(1 for v in vals if significant_digits(v) >= PRECISE_DIGITS) >= MIN_PRECISE_VALUES


def pool_of(value: Any) -> list[float]:
    return sorted(x for _, vec in numeric_fields(value) for x in vec)


def field_match(vals: list[float], pool: list[float], rtol: float, atol: float) -> float:
    """Fraction of *vals* that occur in the sorted *pool* within tolerance."""
    if not vals:
        return 0.0
    hit = 0
    for v in vals:
        tol = atol + rtol * abs(v)
        i = bisect.bisect_left(pool, v - tol)
        if i < len(pool) and pool[i] <= v + tol:
            hit += 1
    return hit / len(vals)


def canonical_text(t: str) -> str:
    """XML-ish text with the declaration, inter-tag whitespace and runs of blanks removed."""
    t = _XML_DECL_RE.sub("", t)
    t = _GAP_RE.sub("><", _WS_RE.sub(" ", t).strip())
    return t.strip()


def compare(name: str, r_val: Any, py_val: Any, rtol: float, atol: float) -> tuple[float, str, str | None, str]:
    """(score, verdict, failure_tag, explanation); verdict ``skip`` when nothing informative can be compared."""
    fields = [(p, v) for p, v in numeric_fields(r_val) if informative(v)]
    if fields:
        pool = pool_of(py_val)
        if not pool and not texts(py_val):
            return 0.0, "fail", "value", f"{name}: Python has no numbers to compare with the R object's {len(fields)} numeric field(s)"
        got = {p: field_match(v, pool, rtol, atol) for p, v in fields}
        weights = {p: min(len(v), MAX_FIELD_WEIGHT) for p, v in fields}
        score = sum(weights[p] * got[p] for p in got) / sum(weights.values())   # a field found in part earns that part
        missing = [p or "(value)" for p in got if got[p] < MATCH_FRACTION]
        if score >= 1.0 - 1e-9:
            return 1.0, "pass", None, ""
        return score, "fail", "value", (
            f"{name}: {len(fields) - len(missing)}/{len(fields)} numeric fields of the R object found in the Python object "
            f"(not found: {', '.join(missing[:6])})")
    r_texts = [canonical_text(t) for t in texts(r_val)]
    r_texts = [t for t in r_texts if t]
    if r_texts:
        py_texts = [canonical_text(t) for t in texts(py_val)]
        if not py_texts:
            return 0.0, "fail", "value", f"{name}: Python has no text form to compare with the R object's"
        best = max(1.0 if a == b else _difflib_similarity(a[:5000], b[:5000]) for a in r_texts for b in py_texts)
        if best >= 1.0:
            return 1.0, "pass", None, ""
        # Partial credit for near matches (the search needs a gradient), but a one-in-ten mismatch must cost.
        return best ** 4, "fail", "value", (
            f"{name}: text forms differ (similarity {best:.2f}) - R {r_texts[0][:80]!r} Python {py_texts[0][:80]!r}")
    return 0.0, "skip", None, f"{name}: no informative numbers or text to compare"

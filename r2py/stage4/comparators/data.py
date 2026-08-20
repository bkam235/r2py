"""Data comparator — exact-first with data_compare fallback (§7.3.1).

Failure tags:
  "value" — the numbers/strings actually differ; never rescued by fallback.
  "infra"  — structurally uncomparable (type mismatch, column-set mismatch,
             serialisation quirk); eligible for embedding fallback under "auto".

data_compare modes:
  "exact"     — infra failures stay fail; no fallback.
  "embedding" — always score by text fallback (v0.1 behaviour; for debugging).
  "auto"      — exact first; rescue only infra-tagged failures via text fallback.
"""
from __future__ import annotations

import math
from typing import Any

from ...types import ComparatorResult, EffectClass
from .base import text_similarity

_DEFAULT_RTOL = 1e-6
_DEFAULT_ATOL = 1e-9
_PREVIEW_MAX = 120   # max chars in a value preview shown in feedback


# ---------------------------------------------------------------------------
# Value preview helper
# ---------------------------------------------------------------------------

def _preview(val: Any, max_chars: int = _PREVIEW_MAX) -> str:
    """Truncated repr of a value for inclusion in feedback messages."""
    r = repr(val)
    if len(r) <= max_chars:
        return r
    return r[:max_chars] + "…"


# ---------------------------------------------------------------------------
# Type helpers
# ---------------------------------------------------------------------------

def _is_numeric(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _is_null(v: Any) -> bool:
    return v is None or (isinstance(v, float) and math.isnan(v))


def _numeric_equal(a: Any, b: Any, rtol: float, atol: float) -> bool:
    if _is_null(a) and _is_null(b):
        return True
    if _is_null(a) or _is_null(b):
        return False
    return abs(a - b) <= atol + rtol * abs(b)


# ---------------------------------------------------------------------------
# Per-value comparison: returns (score, verdict, failure_tag, explanation)
# ---------------------------------------------------------------------------

def _compare_callable_meta(
    name: str,
    r_meta: dict[str, Any],
    py_meta: dict[str, Any],
) -> tuple[float, str, str | None, str]:
    """Compare callable metadata dicts from R and Python sides."""
    score = 0.0

    r_formals = r_meta.get("formals", [])
    py_formals = py_meta.get("formals", [])
    r_clean = [f for f in r_formals if f != "..."]
    py_clean = [f for f in py_formals if f not in ("args", "kwargs")]

    if r_clean == py_clean:
        score += 0.7
    elif r_clean and py_clean:
        common = len(set(r_clean) & set(py_clean))
        total = max(len(r_clean), len(py_clean))
        score += 0.7 * (common / total) if total > 0 else 0.0

    r_attrs = r_meta.get("attributes", {})
    py_attrs = py_meta.get("attributes", {})
    if r_attrs and py_attrs:
        common_keys = set(r_attrs.keys()) & set(py_attrs.keys())
        if common_keys:
            matches = sum(1 for k in common_keys if r_attrs[k] == py_attrs[k])
            score += 0.3 * (matches / len(common_keys))
        else:
            score += 0.15
    elif not r_attrs and not py_attrs:
        score += 0.3

    if score >= 0.95:
        return 1.0, "pass", None, ""

    explanation = (
        f"{name}: callable meta — formals R={r_formals} Py={py_formals}, "
        f"attrs R={list(r_attrs.keys())} Py={list(py_attrs.keys())}, score={score:.3f}"
    )
    if score >= 0.5:
        return score, "fail", "infra", explanation
    return score, "fail", "value", explanation


def _compare_pair(
    name: str,
    r_val: Any,
    py_val: Any,
    rtol: float,
    atol: float,
) -> tuple[float, str, str | None, str]:
    """Compare a single variable's R value vs Python value.

    Returns (score, verdict, failure_tag, explanation).
    verdict is one of: "pass", "fail".
    failure_tag is "value" or "infra" (only on fail), or None on pass.
    """
    # Both null/None
    if _is_null(r_val) and _is_null(py_val):
        return 1.0, "pass", None, ""

    # One null, other not → value failure
    if _is_null(r_val) or _is_null(py_val):
        return 0.0, "fail", "value", f"{name}: one side is null/None, other is not"

    # Both bool
    if isinstance(r_val, bool) and isinstance(py_val, bool):
        if r_val == py_val:
            return 1.0, "pass", None, ""
        return 0.0, "fail", "value", f"{name}: bool {r_val!r} != {py_val!r}"

    # R logical ↔ Python int cross-type (e.g. R TRUE→1 via jsonlite coercion).
    # Treat as compatible; compare by numeric value so 1==True and 0==False.
    if isinstance(r_val, bool) and _is_numeric(py_val):
        expected = 1 if r_val else 0
        if _numeric_equal(expected, py_val, rtol, atol):
            return 1.0, "pass", None, ""
        return 0.0, "fail", "value", f"{name}: bool {r_val!r} (→{expected}) != {py_val!r}"
    if _is_numeric(r_val) and isinstance(py_val, bool):
        expected = 1 if py_val else 0
        if _numeric_equal(r_val, expected, rtol, atol):
            return 1.0, "pass", None, ""
        return 0.0, "fail", "value", f"{name}: {r_val!r} != bool {py_val!r} (→{expected})"

    # Both numeric scalar (R may send int or float from JSON)
    if _is_numeric(r_val) and _is_numeric(py_val):
        if _numeric_equal(r_val, py_val, rtol, atol):
            return 1.0, "pass", None, ""
        return 0.0, "fail", "value", f"{name}: {r_val} != {py_val} (outside tolerance)"

    # Both string
    if isinstance(r_val, str) and isinstance(py_val, str):
        if r_val == py_val:
            return 1.0, "pass", None, ""
        return 0.0, "fail", "value", f"{name}: {r_val!r} != {py_val!r}"

    # Both list (R vector)
    if isinstance(r_val, list) and isinstance(py_val, list):
        if len(r_val) != len(py_val):
            return 0.0, "fail", "infra", (
                f"{name}: length {len(r_val)} vs {len(py_val)}"
                f" — R={_preview(r_val)} Python={_preview(py_val)}"
            )
        for i, (rv, pv) in enumerate(zip(r_val, py_val)):
            elem_score, elem_verdict, elem_tag, elem_expl = _compare_pair(
                f"{name}[{i}]", rv, pv, rtol, atol
            )
            if elem_verdict == "fail":
                return 0.0, "fail", elem_tag, elem_expl
        return 1.0, "pass", None, ""

    # Both dicts with callable metadata sentinel
    if (isinstance(r_val, dict) and isinstance(py_val, dict)
            and r_val.get("__r2py_callable_meta__") and py_val.get("__r2py_callable_meta__")):
        return _compare_callable_meta(name, r_val, py_val)

    # Both dict (R data.frame stored as dict-of-columns, or named list)
    if isinstance(r_val, dict) and isinstance(py_val, dict):
        r_cols = set(r_val.keys())
        py_cols = set(py_val.keys())
        if r_cols != py_cols:
            return 0.0, "fail", "infra", (
                f"{name}: column sets differ — only_r={sorted(r_cols - py_cols)}"
                f" only_py={sorted(py_cols - r_cols)}"
                f" — R={_preview(r_val)} Python={_preview(py_val)}"
            )
        for col in sorted(r_cols):
            col_score, col_verdict, col_tag, col_expl = _compare_pair(
                f"{name}.{col}", r_val[col], py_val[col], rtol, atol
            )
            if col_verdict == "fail":
                return 0.0, "fail", col_tag, col_expl
        return 1.0, "pass", None, ""

    # Type mismatch — structural infra failure
    return 0.0, "fail", "infra", (
        f"{name}: type mismatch — R={type(r_val).__name__} {_preview(r_val)}"
        f" Python={type(py_val).__name__} {_preview(py_val)}"
    )


def _text_fallback(r_val: Any, py_val: Any) -> float:
    """Embedding-stand-in fallback: text similarity of str representations."""
    return text_similarity(str(r_val), str(py_val))


# ---------------------------------------------------------------------------
# DataComparator
# ---------------------------------------------------------------------------

class DataComparator:
    effect_class = EffectClass.DATA

    def __init__(
        self,
        data_compare: str = "auto",
        rtol: float = _DEFAULT_RTOL,
        atol: float = _DEFAULT_ATOL,
    ) -> None:
        if data_compare not in ("auto", "exact", "embedding"):
            raise ValueError(f"data_compare must be 'auto', 'exact', or 'embedding'; got {data_compare!r}")
        self.data_compare = data_compare
        self.rtol = rtol
        self.atol = atol

    def compare(
        self,
        r_effect: dict[str, Any],
        py_effect: dict[str, Any],
        uncapturable: list[str] | None = None,
    ) -> ComparatorResult:
        """Compare two data dicts (var_name → value).

        uncapturable: variable names flagged as uncapturable in the Python bundle;
        these are excluded from the score and listed as uncomparable.
        """
        uncapturable = uncapturable or []

        if not r_effect and not py_effect:
            return ComparatorResult(effect_class=EffectClass.DATA, score=1.0, verdict="pass")

        scores: list[float] = []
        per_variable: dict[str, float] = {}
        explanations: list[str] = []
        uncomparable_vars: list[str] = []
        any_fallback = False

        for name, r_val in r_effect.items():
            if name in uncapturable:
                print(f"[r2py] WARNING: '{name}' is a data entity but Python could not serialize it — excluded from comparison", flush=True)
                uncomparable_vars.append(name)
                continue

            if self.data_compare == "embedding":
                # Always use text fallback (v0.1 mode).
                # Guard against missing variable before falling back.
                if name not in py_effect:
                    scores.append(0.0)
                    per_variable[name] = 0.0
                    explanations.append(f"{name}: missing in Python output (R={_preview(r_val)})")
                    continue
                fb_score = _text_fallback(r_val, py_effect[name])
                scores.append(fb_score)
                per_variable[name] = fb_score
                if fb_score < 1.0:
                    explanations.append(f"{name}: fallback similarity {fb_score:.3f}")
                any_fallback = True
                continue

            py_val = py_effect.get(name)
            if py_val is None and name not in py_effect:
                # Variable missing entirely from Python output
                scores.append(0.0)
                per_variable[name] = 0.0
                explanations.append(f"{name}: missing in Python output (R={_preview(r_val)})")
                continue

            score, verdict, failure_tag, explanation = _compare_pair(
                name, r_val, py_val, self.rtol, self.atol
            )

            if verdict == "fail" and failure_tag == "infra" and self.data_compare == "auto":
                # Rescue infra failures via text fallback; value failures are never rescued
                fb_score = _text_fallback(r_val, py_val)
                scores.append(fb_score)
                per_variable[name] = fb_score
                if fb_score > 0.0:
                    explanations.append(
                        f"{name}: infra failure rescued by fallback (score {fb_score:.3f}): {explanation}"
                    )
                    any_fallback = True
                else:
                    explanations.append(f"{name}: {explanation}")
            else:
                scores.append(score)
                per_variable[name] = score
                if verdict == "fail":
                    explanations.append(f"{name}: {explanation}")

        # Variables only in Python (not in R) are ignored per architecture spec

        if not scores and uncomparable_vars:
            return ComparatorResult(
                effect_class=EffectClass.DATA,
                score=0.0,
                verdict="uncomparable",
                explanation=f"all variables uncomparable: {uncomparable_vars}",
            )

        if not scores:
            # No R variables to compare against
            return ComparatorResult(effect_class=EffectClass.DATA, score=1.0, verdict="pass")

        avg_score = sum(scores) / len(scores)

        if any_fallback and avg_score >= 0.9:
            verdict = "pass_via_fallback"
        elif avg_score >= 1.0:
            verdict = "pass"
        else:
            verdict = "fail"

        return ComparatorResult(
            effect_class=EffectClass.DATA,
            score=avg_score,
            verdict=verdict,
            explanation="; ".join(explanations) if explanations else "",
            failure_tag="value" if verdict == "fail" else None,
            per_variable=per_variable,
        )

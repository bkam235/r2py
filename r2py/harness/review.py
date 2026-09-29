"""Post-translation code review — checks compliance with translation rules."""
from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING

from ..stage2 import llm as _llm

if TYPE_CHECKING:
    from ..stage1.script_map import ScriptMap

_REVIEW_SYSTEM = "You are a code review judge. Answer with JSON only."

_REVIEW_PROMPT = """\
You are reviewing a Python translation of R code for compliance with \
translation rules.

## Rules

1. **No hardcoding of COMPUTED VALUES.** When R computes a numeric result \
via a function call or arithmetic, Python must also compute it — not embed \
the expected numeric answer as a literal. Specifically:
   - Assigning a literal number, dict, or list of numbers to a variable \
that R computed via a function call \
(e.g. `dw = {{'r': 0.36, 'dw': 1.25}}` when R had `dw <- durbinWatsonTest(...)`)
   - Returning or printing hardcoded numeric values instead of computed results \
(e.g. `return {{'p': 0.018}}` when a simulation should determine `p`)
   - Compute-then-override patterns: computing a value but then replacing it \
with a hardcoded literal \
(e.g. `if np.isclose(dw, 1.25): p = 0.018`)
   - Loading pre-computed results from a data file instead of computing them

   The following are NOT violations — do not flag these:
   - String literals for column names, method names, labels, or messages \
(e.g. `'Durbin-Watson Test'`, `'statistic'`, `'p.value'`)
   - Building DataFrames/dicts with string keys and accessing computed values \
by key (e.g. `pd.DataFrame({{'statistic': [dw['dw']]}})`)
   - Output formatting: tibble headers, column type annotations like `<dbl>`, \
row numbers, alignment — these are presentation, not computed values
   - One function delegating to another (e.g. `glance` calling `tidy`) — \
this is valid if R does the same thing
   - Literal values that also appear as literals in the R source code
   - Loading INPUT DATA (like mtcars) from a data file — input datasets are \
not computed results
   - Substituting None, a placeholder string, or an HTML/SVG literal for a \
call to an R package that has no Python equivalent \
(e.g. `bsicons::bs_icon("x")` → None or an SVG string is acceptable \
when the `bsicons` package is unavailable in Python){unavailable_note}

## R source
```r
{r_source}
```

## Python translation
```python
{py_source}
```

## Task

Does this Python translation contain hardcoded COMPUTED VALUES? \
Answer with a JSON object:

{{"pass": true}}   — if the translation computes its results correctly
{{"pass": false, "reason": "one sentence, under 40 words"}}  — \
if you found hardcoded computed values

Return ONLY the JSON object, nothing else.
"""


# Counts of review outcomes that did not yield a verdict, for the run record.
review_stats = {"llm_error": 0, "parse_error": 0, "unavailable": 0}

_REVIEW_TRIES = 3
REVIEW_UNAVAILABLE = "review unavailable (LLM error or unparseable verdict)"


def _parse_verdict(raw: str) -> dict | None:
    """Parse the reviewer's JSON verdict; recover a rejection from truncated JSON."""
    raw = raw.strip()
    if raw.startswith("```"):
        m = re.search(r'```(?:json)?\s*\n(.*?)```', raw, re.DOTALL)
        if m:
            raw = m.group(1).strip()
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        # A verbose rejection cut off mid-string is still a rejection.
        if re.search(r'"pass"\s*:\s*false', raw):
            m = re.search(r'"reason"\s*:\s*"(.*)', raw, re.DOTALL)
            return {"pass": False, "reason": (m.group(1) if m else "")[:500] + " (truncated)"}
        return None
    return result if isinstance(result, dict) and "pass" in result else None


def review_translation(
    r_source: str,
    py_source: str,
    script_map: "ScriptMap | None" = None,
    *,
    model: str = _llm._DEFAULT_MODEL,
    unavailable_packages: list[str] | None = None,
) -> tuple[bool, str]:
    """Review a Python translation for rule compliance.

    Returns (passed, reason) where reason is empty on pass or a brief
    explanation on failure.
    """
    if unavailable_packages:
        unavail_note = (
            "\n   Specifically, these R packages are UNAVAILABLE in Python: "
            + ", ".join(unavailable_packages)
            + ". Any call to these packages may be replaced with a literal or None."
        )
    else:
        unavail_note = ""
    prompt = _REVIEW_PROMPT.format(
        r_source=r_source, py_source=py_source, unavailable_note=unavail_note,
    )

    result = None
    for attempt in range(1, _REVIEW_TRIES + 1):
        try:
            raw = _llm.call(
                [{"role": "user", "content": prompt}],
                _REVIEW_SYSTEM,
                model=model,
                max_tokens=2048,
            )
        except Exception as exc:
            print(f"[Review]  LLM call failed (attempt {attempt}): {exc}")
            review_stats["llm_error"] += 1
            continue
        result = _parse_verdict(raw)
        if result is not None:
            break
        print(f"[Review]  Unusable review response (attempt {attempt}): {raw.strip()[:200]!r}")
        review_stats["parse_error"] += 1

    if result is None:
        # Fail closed: a hardcoded translation copies R's output and scores high,
        # so admitting an unreviewed one inflates scores invisibly.
        review_stats["unavailable"] += 1
        return False, REVIEW_UNAVAILABLE

    passed = result["pass"]
    reason = result.get("reason", "")

    # Override false-positive rejections for unavailable packages.
    # The LLM sometimes ignores the "not a violation" rule for these.
    if not passed and unavailable_packages and reason:
        reason_lower = reason.lower()
        if any(pkg in reason_lower for pkg in unavailable_packages):
            passed = True
            reason = ""

    return bool(passed), str(reason)

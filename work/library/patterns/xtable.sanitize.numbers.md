---
id: xtable.sanitize.numbers
package: xtable
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# xtable.sanitize.numbers

## Guidance
Translate R `sanitize.numbers` (FunctionCall from xtable) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "2236c69e", "r_snippet": "sanitize.numbers(x, \"latex\", TRUE)", "py_snippet": "def sanitize_numbers(str_val, type_val, math_style_negative=False, math_style_exponents=False):\n    \"\"\"Implementation of xtable::sanitize.numbers\"\"\"\n    if not isinstance(str_val, (list, np.ndarray)):\n        str_val = [str_val]\n    else:\n        str_val = list(str_val)\n    \n    # R's as.character(x) for numbers doesn't truncate as aggressively as Python's str() or float formatting\n    # We use format(s, '.15g') to better mimic R's default number-to-string conversion\n    result = [format(s, '.15g') for s in str_val]\n    \n    if type_val == \"latex\":\n        if math_style_negative:\n            r", "score": 0.8021, "script_id": "auto"}

## Edit Examples
(none)

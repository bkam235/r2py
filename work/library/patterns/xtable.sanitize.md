---
id: xtable.sanitize
package: xtable
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# xtable.sanitize

## Guidance
Translate R `sanitize` (FunctionCall from xtable) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "d0092cf0", "r_snippet": "sanitize(insane, type = \"latex\")", "py_snippet": "def sanitize(str_val, type_val=\"latex\"):\n    \"\"\"Implementation of xtable::sanitize\"\"\"\n    if isinstance(str_val, (list, np.ndarray)):\n        return np.array([sanitize(s, type_val) for s in str_val])\n    \n    if not isinstance(str_val, str):\n        str_val = str(str_val)\n\n    if type_val == \"latex\":\n        result = str_val\n        result = result.replace(\"\\\\\", \"SANITIZE.BACKSLASH\")\n        result = result.replace(\"$\", r\"\\$\")\n        result = result.replace(\">\", r\"$>$\")\n        result = result.replace(\"<\", r\"$<$\")\n        result = result.replace(\"|\", r\"$|$\")\n        result = result.replace(\"{", "score": 0.9848, "script_id": "auto"}

## Edit Examples
(none)

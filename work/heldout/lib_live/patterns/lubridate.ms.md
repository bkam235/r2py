---
id: lubridate.ms
package: lubridate
confidence: tentative
seed: true
created: 2026-09-22
last_review: 2026-09-22
tie_count: 0
---

# lubridate.ms

## Guidance
Translate R `ms` (FunctionCall from lubridate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "eaa1fb28", "r_snippet": "ms(c(\"09:10\", \"09:02\", \"1:10\"))", "py_snippet": "def ms(*args, quiet=False, roll=False):\n    # R's ... handles both vectors and multiple arguments\n    inputs = []\n    for arg in args:\n        if isinstance(arg, (list, np.ndarray, pd.Series)):\n            inputs.extend(arg)\n        else:\n            inputs.append(arg)\n    \n    return _parse_hms_logic(inputs, \"MS\")\n\nres_ms = ms([\"09:10\", \"09:02\", \"1:10\"])\nprint(format_r_vector(res_ms))", "score": 1.0, "script_id": "lubridate__rd_example__hms_Rd", "n_calls": 0}

## Edit Examples
(none)

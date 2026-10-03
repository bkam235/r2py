---
id: lubridate.hm
package: lubridate
confidence: tentative
seed: true
created: 2026-09-22
last_review: 2026-09-22
tie_count: 0
---

# lubridate.hm

## Guidance
Translate R `hm` (FunctionCall from lubridate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "4be6f372", "r_snippet": "hm(c(\"09:10\", \"09:02\", \"1:10\"))", "py_snippet": "def hm(*args, quiet=False, roll=False):\n    inputs = []\n    for arg in args:\n        if isinstance(arg, (list, np.ndarray, pd.Series)):\n            inputs.extend(arg)\n        else:\n            inputs.append(arg)\n            \n    return _parse_hms_logic(inputs, \"HM\")\n\nres_hm = hm([\"09:10\", \"09:02\", \"1:10\"])\nprint(format_r_vector(res_hm))", "score": 0.9203, "script_id": "lubridate__rd_example__hms_Rd", "n_calls": 0}

## Edit Examples
(none)

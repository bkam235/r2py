---
id: lubridate.minute
package: lubridate
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# lubridate.minute

## Guidance
Translate R `minute` (FunctionCall from lubridate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "6e69a025", "r_snippet": "minute(x)", "py_snippet": "def minute(x):\n    if isinstance(x, pd.Timestamp):\n        return x.minute\n    return None\n\nprint(minute(x))\n\n# minute(x) <- 1", "score": 1.0, "script_id": "lubridate__rd_example__minute_Rd", "n_calls": 0}

## Edit Examples
(none)

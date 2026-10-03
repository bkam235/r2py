---
id: base.as.date
package: base
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# base.as.date

## Guidance
Translate R `as.Date` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "190b92d4", "r_snippet": "x <- as.Date(\"2019-01-01\")", "py_snippet": "x = pd.to_datetime(\"2019-01-01\").date()\n\n# as_naive_time(x)", "score": 1.0, "script_id": "clock__rd_example__as_naive_time_Rd", "n_calls": 1}

## Edit Examples
(none)

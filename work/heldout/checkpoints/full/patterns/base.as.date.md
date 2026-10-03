---
id: base.as.date
package: base
confidence: tentative
seed: true
created: 2026-09-24
last_review: 2026-09-24
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
- {"r_hash": "e1b5e8f8", "r_snippet": "x <- as.Date(\"2009-08-02\")", "py_snippet": "x = pd.to_datetime(\"2009-08-02\").date()", "score": 1.0, "script_id": "lubridate__rd_example__leap_year_Rd", "n_calls": 1}

## Edit Examples
(none)

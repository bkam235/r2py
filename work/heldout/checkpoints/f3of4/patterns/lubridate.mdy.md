---
id: lubridate.mdy
package: lubridate
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# lubridate.mdy

## Guidance
Translate R `mdy` (FunctionCall from lubridate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "df41c4cd", "r_snippet": "mdy(\"06-04-2011\")", "py_snippet": "print(pd.to_datetime(\"06-04-2011\", format=\"%m-%d-%Y\").strftime(\"%Y-%m-%d\"))", "score": 1.0, "script_id": "lubridate__vignette__lubridate_s2", "n_calls": 0}

## Edit Examples
(none)

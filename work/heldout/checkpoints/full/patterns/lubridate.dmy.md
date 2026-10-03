---
id: lubridate.dmy
package: lubridate
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# lubridate.dmy

## Guidance
Translate R `dmy` (FunctionCall from lubridate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "912b9684", "r_snippet": "dmy(\"04/06/2011\")", "py_snippet": "print(pd.to_datetime(\"04/06/2011\", format=\"%d/%m/%Y\").strftime(\"%Y-%m-%d\"))", "score": 1.0, "script_id": "lubridate__vignette__lubridate_s2", "n_calls": 0}

## Edit Examples
(none)

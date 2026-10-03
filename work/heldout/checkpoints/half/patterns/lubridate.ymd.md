---
id: lubridate.ymd
package: lubridate
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# lubridate.ymd

## Guidance
Translate R `ymd` (FunctionCall from lubridate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e3e59623", "r_snippet": "ymd(\"20110604\")", "py_snippet": "print(pd.to_datetime(\"20110604\", format=\"%Y%m%d\").strftime(\"%Y-%m-%d\"))", "score": 1.0, "script_id": "lubridate__vignette__lubridate_s2", "n_calls": 0}

## Edit Examples
(none)

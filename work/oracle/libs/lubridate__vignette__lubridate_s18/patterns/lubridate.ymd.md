---
id: lubridate.ymd
package: lubridate
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# lubridate.ymd

## Guidance
Translate R `ymd` from lubridate to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e3e59623", "r_snippet": "ymd(\"20110604\")", "py_snippet": "print(pd.to_datetime(\"20110604\", format=\"%Y%m%d\").strftime(\"%Y-%m-%d\"))", "score": 1.0, "script_id": "lubridate__vignette__lubridate_s2.R", "n_calls": 0}

## Edit Examples
(none)

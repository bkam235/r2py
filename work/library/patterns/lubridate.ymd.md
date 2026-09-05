---
id: lubridate.ymd
package: lubridate
confidence: tentative
seed: true
created: 2026-09-05
last_review: 2026-09-05
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
- {"r_hash": "e3e59623", "r_snippet": "ymd(\"20110604\")", "py_snippet": "def ymd(x, quiet=False, tz=None, locale=None, truncated=0):\n    return pd.to_datetime(x, format='%Y%m%d')\n\nprint(ymd(\"20110604\"))", "score": 0.8704, "script_id": "auto"}

## Edit Examples
(none)

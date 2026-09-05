---
id: lubridate.dmy
package: lubridate
confidence: tentative
seed: true
created: 2026-09-05
last_review: 2026-09-05
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
- {"r_hash": "912b9684", "r_snippet": "dmy(\"04/06/2011\")", "py_snippet": "def dmy(x, quiet=False, tz=None, locale=None, truncated=0):\n    return pd.to_datetime(x, format='%d/%m/%Y')\n\nprint(dmy(\"04/06/2011\"))", "score": 0.8704, "script_id": "auto"}

## Edit Examples
(none)

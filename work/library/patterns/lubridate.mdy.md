---
id: lubridate.mdy
package: lubridate
confidence: tentative
seed: true
created: 2026-09-05
last_review: 2026-09-05
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
- {"r_hash": "df41c4cd", "r_snippet": "mdy(\"06-04-2011\")", "py_snippet": "def mdy(x, quiet=False, tz=None, locale=None, truncated=0):\n    return pd.to_datetime(x, format='%m-%d-%Y')\n\nprint(mdy(\"06-04-2011\"))", "score": 0.8704, "script_id": "auto"}

## Edit Examples
(none)

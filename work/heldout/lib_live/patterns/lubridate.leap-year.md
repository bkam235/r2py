---
id: lubridate.leap-year
package: lubridate
confidence: tentative
seed: true
created: 2026-09-24
last_review: 2026-09-24
tie_count: 0
---

# lubridate.leap-year

## Guidance
Translate R `leap_year` (FunctionCall from lubridate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "67884407", "r_snippet": "leap_year(x) # FALSE", "py_snippet": "def leap_year(x):\n    if isinstance(x, (int, np.integer)):\n        return calendar.isleap(int(x))\n    elif isinstance(x, (pd.Timestamp, date)):\n        return calendar.isleap(x.year)\n    else:\n        # Handle string dates by converting to pandas timestamp\n        ts = pd.to_datetime(x)\n        return calendar.isleap(ts.year)\n\nprint(leap_year(x)) # False", "score": 1.0, "script_id": "lubridate__rd_example__leap_year_Rd", "n_calls": 0}

## Edit Examples
(none)

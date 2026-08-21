---
id: clock.date-build
package: clock
confidence: tentative
seed: true
created: 2026-07-06
last_review: 2026-07-06
tie_count: 0
---

# clock.date-build

## Guidance
Translate R `date_build` (FunctionCall from clock) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "fee1f507", "r_snippet": "set_hour(y, 2, nonexistent = \"roll-forward\")", "py_snippet": "def set_hour(dt, hour, nonexistent=\"error\"):\n    try:\n        return dt.replace(hour=hour)\n    except (ValueError, OSError):\n        if nonexistent == \"roll-forward\":\n            # Roll forward: move to the start of the next valid time (usually +1 hour)\n            return dt.replace(hour=hour) + timedelta(hours=1)\n        elif nonexistent == \"roll-backward\":\n            # Roll backward: move to the last valid time before the gap\n            return dt.replace(hour=hour) - timedelta(hours=1)\n        raise\n\n# x <- as.POSIXct(\"2019-02-01\", tz = \"America/New_York\")\n\nprint(set_hour(y, 2, nonexistent", "score": 0.8953, "script_id": "auto"}
- {"r_hash": "757f6fa6", "r_snippet": "set_day(x, \"last\")", "py_snippet": "print(set_day(x, \"last\"))\n\n# try(set_day(x, 31))", "score": 0.8056, "script_id": "auto"}
- {"r_hash": "12084efa", "r_snippet": "date_build(2019, 1:12, 31)", "py_snippet": "try:\n    # Pandas.to_datetime handles date construction. \n    # Using a dataframe to simulate the vectorization of 1:12\n    dates = pd.to_datetime({'year': 2019, 'month': np.arange(1, 13), 'day': 31}, errors='coerce')\nexcept Exception:\n    pass", "score": 0.8, "script_id": "auto"}

## Edit Examples
(none)

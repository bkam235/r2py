---
id: clock.as-naive-time
package: clock
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# clock.as-naive-time

## Guidance
Translate R `as_naive_time` (FunctionCall from clock) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "18721e41", "r_snippet": "as_naive_time(x)", "py_snippet": "def as_naive_time(x):\n    if isinstance(x, date):\n        res = pd.Timestamp(x)\n        print(\"<naive_time<day>[1]>\")\n        print(f'[1] \"{res.strftime(\"%Y-%m-%d\")}\"')\n        return res\n    elif isinstance(x, YearMonthDay):\n        if x.precision != \"day\":\n            raise ValueError(\"A minimum of day precision is required\")\n        res = pd.Timestamp(year=x.year, month=x.month, day=x.day)\n        print(\"<naive_time<day>[1]>\")\n        print(f'[1] \"{res.strftime(\"%Y-%m-%d\")}\"')\n        return res\n    else:\n        raise TypeError(f\"Can't perform this operation on a {type(x)}.\")\n\n# suppressPackageStartupMessages(library(clock))\npass\n\n# x <- as.Date(\"2019-01-01\")\n\nas_naive_time(x)\n\n# ym <- year_month_day(2019, 02)", "score": 1.0, "script_id": "clock__rd_example__as_naive_time_Rd", "n_calls": 0}

## Edit Examples
(none)

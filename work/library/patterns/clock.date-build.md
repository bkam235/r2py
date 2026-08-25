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
- {"r_hash": "9a2893c0", "r_snippet": "as_weekday(x)", "py_snippet": "def as_weekday(x):\n    # R clock: Sunday=1, Monday=2, ..., Saturday=7\n    # Python isoweekday: Monday=1, ..., Sunday=7\n    def map_weekday(dt):\n        iso = dt.isoweekday()\n        return iso + 1 if iso < 7 else 1\n    \n    res = [map_weekday(dt) for dt in x]\n    # Format for printing to match R output style: <weekday[n]> [Tue Wed]\n    return res\n\nprint(format_clock_output(as_weekday(x), \"weekday\"))", "score": 1.0, "script_id": "auto"}
- {"r_hash": "0fbb8a35", "r_snippet": "time_point_shift(x, monday)", "py_snippet": "def time_point_shift(x, target, which=\"next\", boundary=\"keep\"):\n    res = []\n    for dt in x:\n        # Current weekday: Sun=1, Mon=2, ...\n        current_wd = (dt.isoweekday() + 1) if dt.isoweekday() < 7 else 1\n        \n        work_dt = dt\n        if which == \"next\":\n            if boundary == \"advance\":\n                work_dt = work_dt + timedelta(days=1)\n            \n            # Recalculate current_wd if advanced\n            curr = (work_dt.isoweekday() + 1) if work_dt.isoweekday() < 7 else 1\n            diff = target - curr\n            if diff < 0:\n                diff += 7\n           ", "score": 1.0, "script_id": "auto"}
- {"r_hash": "fee1f507", "r_snippet": "set_hour(y, 2, nonexistent = \"roll-forward\")", "py_snippet": "def set_hour(dt, hour, nonexistent=\"error\"):\n    try:\n        return dt.replace(hour=hour)\n    except (ValueError, OSError):\n        if nonexistent == \"roll-forward\":\n            # Roll forward: move to the start of the next valid time (usually +1 hour)\n            return dt.replace(hour=hour) + timedelta(hours=1)\n        elif nonexistent == \"roll-backward\":\n            # Roll backward: move to the last valid time before the gap\n            return dt.replace(hour=hour) - timedelta(hours=1)\n        raise\n\n# x <- as.POSIXct(\"2019-02-01\", tz = \"America/New_York\")\n\nprint(set_hour(y, 2, nonexistent", "score": 0.8953, "script_id": "auto"}

## Edit Examples
(none)

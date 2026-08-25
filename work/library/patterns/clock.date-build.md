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
- {"r_hash": "219623a2", "r_snippet": "date_format(x)", "py_snippet": "print(x.strftime('%Y-%m-%d'))\n\n# date_format(x, format = \"year: %Y, month: %m, day: %d\")", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

---
id: base.seq
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.seq

## Guidance
Translate R `seq` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "2483263c", "r_snippet": "seq(\n  as_naive_time(year_month_day(2019, 1, 1)),\n  as_naive_time(year_month_day(2019, 2, 4)),\n  by = 5\n)", "py_snippet": "    return x\n\n# Daily sequence\nstart_1 = as_naive_time(year_month_day(2019, 1, 1))\nend_1 = as_naive_time(year_month_day(2019, 2, 4))", "score": 1.0, "script_id": "clock__rd_example__seq_clock_time_point_Rd.R", "n_calls": 1}
- {"r_hash": "c6e89170", "r_snippet": "seq(x, by = 4, length.out = 10)", "py_snippet": "x = as_naive_time(year_month_day(2019, 1, 2, 3, 3))\nclock_print([x.strftime('%Y-%m-%dT%H:%M')], \"minute\")", "score": 1.0, "script_id": "clock__rd_example__seq_clock_time_point_Rd.R", "n_calls": 1}

## Edit Examples
(none)

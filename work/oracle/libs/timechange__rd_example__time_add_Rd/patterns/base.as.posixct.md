---
id: base.as.posixct
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.as.posixct

## Guidance
Translate R `as.posixct` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "d53ef083", "r_snippet": "x <- as.POSIXct(\"2009-08-07 00:00:00\", tz = \"America/New_York\")", "py_snippet": "        return localized.time()", "score": 1.0, "script_id": "timechange__rd_example__time-zones_Rd.R", "n_calls": 1}
- {"r_hash": "7f946863", "r_snippet": "y <- as.POSIXct(\"2010-03-14 02:05:05\", tz = \"UTC\")", "py_snippet": "print(time_at_tz(x, \"UTC\"))", "score": 1.0, "script_id": "timechange__rd_example__time-zones_Rd.R", "n_calls": 1}

## Edit Examples
(none)

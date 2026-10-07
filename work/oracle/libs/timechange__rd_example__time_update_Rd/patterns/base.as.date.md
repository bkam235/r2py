---
id: base.as.date
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.as.date

## Guidance
Translate R `as.date` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "568c7be1", "r_snippet": "as.Date(x) # by default as.Date assumes you want to know the date in UTC", "py_snippet": "# as.Date(x) # by default as.Date assumes you want to know the date in UTC\n# R's as.Date(POSIXct) converts to UTC first.", "score": 1.0, "script_id": "lubridate__rd_example__date_Rd.R", "n_calls": 1}
- {"r_hash": "848d7459", "r_snippet": "as.Date(x, tz = \"America/New_York\")", "py_snippet": "r_print_date(x.tz_convert(\"UTC\").date().isoformat())\n\n# as.Date(x, tz = \"America/New_York\")", "score": 1.0, "script_id": "lubridate__rd_example__date_Rd.R", "n_calls": 1}

## Edit Examples
(none)

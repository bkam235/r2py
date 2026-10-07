---
id: base.format
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.format

## Guidance
Translate R `format` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "89977d86", "r_snippet": "format(date)", "py_snippet": "def format(x):\n    return f'\"{x.format_date()}\"'\n\nprint(repr(date))", "score": 1.0, "script_id": "timeDate__rd_example__timeDate-finCenter_Rd.R", "n_calls": 1}

## Edit Examples
(none)

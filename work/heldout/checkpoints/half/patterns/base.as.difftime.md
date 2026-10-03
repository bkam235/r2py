---
id: base.as.difftime
package: base
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# base.as.difftime

## Guidance
Translate R `as.difftime` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "1f4af70c", "r_snippet": "time_ago(now - as.difftime(30, units = \"secs\"))", "py_snippet": "print(time_ago(now - timedelta(seconds=30)))", "score": 1.0, "script_id": "prettyunits__rd_example__time_ago_Rd", "n_calls": 1}

## Edit Examples
(none)

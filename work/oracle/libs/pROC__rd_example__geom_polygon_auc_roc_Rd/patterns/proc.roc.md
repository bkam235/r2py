---
id: proc.roc
package: proc
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# proc.roc

## Guidance
Translate R `roc` from proc to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "4d3be669", "r_snippet": " roc(aSAH$outcome, aSAH$s100b)", "py_snippet": "rocobj = roc(aSAH['outcome'], aSAH['s100b'])\nprint(rocobj)", "score": 1.0, "script_id": "pROC__rd_example__print_Rd.R", "n_calls": 0}

## Edit Examples
(none)

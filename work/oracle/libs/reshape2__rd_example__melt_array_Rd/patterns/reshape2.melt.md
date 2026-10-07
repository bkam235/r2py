---
id: reshape2.melt
package: reshape2
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# reshape2.melt

## Guidance
Translate R `melt` from reshape2 to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "cbd2f18e", "r_snippet": "melt(a)", "py_snippet": "print(melt(a_named))\n\n# a <- list(matrix(1:4, ncol=2), matrix(1:6, ncol=2))", "score": 0.9937, "script_id": "reshape2__rd_example__melt_list_Rd.R", "n_calls": 0}

## Edit Examples
(none)

---
id: base.as.list
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.as.list

## Guidance
Translate R `as.list` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "c12d53a6", "r_snippet": "a <- as.list(c(1:4, NA))", "py_snippet": "a = [1, 2, 3, 4, np.nan]", "score": 1.0, "script_id": "reshape2__rd_example__melt_list_Rd", "n_calls": 1}

## Edit Examples
(none)

---
id: base.array
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.array

## Guidance
Translate R `array` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "4f469a0b", "r_snippet": "a <- list(matrix(1:4, ncol=2), array(1:27, c(3,3,3)))", "py_snippet": "a = [np.arange(1, 5).reshape(2, 2), np.arange(1, 28).reshape(3, 3, 3)]", "score": 1.0, "script_id": "reshape2__rd_example__melt_list_Rd", "n_calls": 2}

## Edit Examples
(none)

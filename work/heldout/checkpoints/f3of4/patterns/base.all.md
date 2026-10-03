---
id: base.all
package: base
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# base.all

## Guidance
Translate R `all` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "505147dd", "r_snippet": "    if (!all(as.matrix(xs) == as.matrix(xs2)))", "py_snippet": "    if not np.array_equal(xs.toarray(), xs2.toarray()):", "score": 1.0, "script_id": "e1071__rd_example__read_matrix_csr_Rd", "n_calls": 2}

## Edit Examples
(none)

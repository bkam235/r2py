---
id: base.as.matrix
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.as.matrix

## Guidance
Translate R `as.matrix` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "75c4ba16", "r_snippet": "    x <- as.matrix(iris[,1:4])", "py_snippet": "    iris_df = pd.DataFrame(iris)\n    \n    # x <- as.matrix(iris[,1:4])", "score": 1.0, "script_id": "e1071__rd_example__read_matrix_csr_Rd.R", "n_calls": 1}
- {"r_hash": "505147dd", "r_snippet": "    if (!all(as.matrix(xs) == as.matrix(xs2)))", "py_snippet": "    write_matrix_csr(xs, y=y, file=\"iris.dat\")", "score": 1.0, "script_id": "e1071__rd_example__read_matrix_csr_Rd.R", "n_calls": 2}

## Edit Examples
(none)

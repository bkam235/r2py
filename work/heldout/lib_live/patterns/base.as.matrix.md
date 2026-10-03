---
id: base.as.matrix
package: base
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# base.as.matrix

## Guidance
Translate R `as.matrix` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "75c4ba16", "r_snippet": "    x <- as.matrix(iris[,1:4])", "py_snippet": "    x = iris_df.iloc[:, 0:4].values\n    \n    # y <- iris[,5]", "score": 1.0, "script_id": "e1071__rd_example__read_matrix_csr_Rd", "n_calls": 1}

## Edit Examples
(none)

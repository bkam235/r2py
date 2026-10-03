---
id: utils.data
package: utils
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# utils.data

## Guidance
Translate R `data` from utils to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "09ddd7c4", "r_snippet": "    data(iris)", "py_snippet": "    iris_df = pd.DataFrame(iris)\n    \n    # x <- as.matrix(iris[,1:4])", "score": 1.0, "script_id": "e1071__rd_example__read_matrix_csr_Rd", "n_calls": 1}

## Edit Examples
- {"failure_class": "variable_output", "old_code": "from sklearn.datasets import load_iris\niris_data = load_iris()\nd = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)", "new_code": "    iris_df = pd.DataFrame(iris)\n    \n    # x <- as.matrix(iris[,1:4])", "score_delta": 0.3328, "script_id": "e1071__rd_example__read_matrix_csr_Rd", "r_snippet": "    data(iris)", "functions": ["utils::data"]}

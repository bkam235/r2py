---
id: sparsevctrs.sparse-subtraction-scalar
package: sparsevctrs
confidence: tentative
seed: true
created: 2026-08-21
last_review: 2026-08-21
tie_count: 0
---

# sparsevctrs.sparse-subtraction-scalar

## Guidance
Translate R `sparse_subtraction_scalar` (FunctionCall from sparsevctrs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "b520b3a8", "r_snippet": "sparse_subtraction_scalar(x_sparse, 2)", "py_snippet": "def sparse_subtraction_scalar(x: SparseVector, val: float):\n    if np.isnan(val):\n        return np.full(x.length, np.nan)\n    if val == 0:\n        return x.to_dense()\n    \n    new_values = x.values - val\n    new_default = x.default - val\n    return sparse_double(new_values, x.positions + 1, x.length, new_default).to_dense()\n\n# Main Execution\n\nprint(format_r_vector(sparse_subtraction_scalar(x_sparse, 2)))", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

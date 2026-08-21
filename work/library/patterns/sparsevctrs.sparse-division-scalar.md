---
id: sparsevctrs.sparse-division-scalar
package: sparsevctrs
confidence: tentative
seed: true
created: 2026-08-21
last_review: 2026-08-21
tie_count: 0
---

# sparsevctrs.sparse-division-scalar

## Guidance
Translate R `sparse_division_scalar` (FunctionCall from sparsevctrs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "3b91528e", "r_snippet": "sparse_division_scalar(x_sparse, 2)", "py_snippet": "def sparse_division_scalar(x: SparseVector, val: float):\n    if np.isnan(val):\n        return np.full(x.length, np.nan)\n    if val == 0:\n        return np.full(x.length, np.inf)\n    if val == 1:\n        return x.to_dense()\n    \n    new_values = x.values / val\n    return sparse_double(new_values, x.positions + 1, x.length, x.default).to_dense()\n\nprint(format_r_vector(sparse_division_scalar(x_sparse, 2)))", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

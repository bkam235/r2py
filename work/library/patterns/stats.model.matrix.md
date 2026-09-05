---
id: stats.model.matrix
package: stats
confidence: tentative
seed: true
created: 2026-09-05
last_review: 2026-09-05
tie_count: 0
---

# stats.model.matrix

## Guidance
Translate R `model.matrix` (FunctionCall from stats) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "c931988d", "r_snippet": "model.matrix(~fail_severity, data = ord_data)", "py_snippet": "def contr_poly(n: int) -> np.ndarray:\n    \"\"\"\n    Programmatically compute R's contr.poly(n) matrix.\n    R's orthogonal polynomial contrasts are based on the \n    discrete orthogonal polynomials on the set {1, ..., n}.\n    \"\"\"\n    # For n levels, there are n-1 contrast columns.\n    # The coefficients are derived from the formula for orthogonal polynomials.\n    # A reliable way to mimic R's contr.poly is to use the \n    # Gram-Schmidt process on the powers of x = [1, ..., n],\n    # then scale the result to match R's specific scaling.\n    \n    x = np.arange(1, n + 1, dtype=float)\n    # Base powe", "score": 0.9667, "script_id": "auto"}

## Edit Examples
(none)

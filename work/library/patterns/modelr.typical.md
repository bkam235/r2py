---
id: modelr.typical
package: modelr
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# modelr.typical

## Guidance
Translate R `typical` (FunctionCall from modelr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "b279df45", "r_snippet": "typical(rpois(100, lambda = 10))", "py_snippet": "def typical(x: Any) -> Any:\n    # Convert to pandas Series for consistent handling\n    if not isinstance(x, pd.Series):\n        s = pd.Series(x)\n    else:\n        s = x\n\n    # Handle ordered categorical (median)\n    if isinstance(s.dtype, pd.CategoricalDtype) and s.dtype.ordered:\n        # R typical for ordered factors returns the median\n        # This is the value at the 50th percentile of the sorted data\n        sorted_s = s.sort_values()\n        n = len(sorted_s)\n        if n == 0:\n            return None\n        \n        # R median for factors: if n is odd, middle element. \n        # If ev", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

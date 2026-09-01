---
id: tidyr.complete
package: tidyr
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# tidyr.complete

## Guidance
Translate R `complete` (FunctionCall from tidyr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "62df284e", "r_snippet": "  complete(x, y)", "py_snippet": "def complete(data, *cols, fill=None, explicit=True):\n    \"\"\"\n    Python implementation of tidyr::complete wrapped in LazyDt.\n    \"\"\"\n    def op(df):\n        # Get unique values for each specified column\n        unique_vals = [df[col].unique() for col in cols]\n        \n        # Create all combinations\n        all_combinations = pd.DataFrame(\n            list(product(*unique_vals)), \n            columns=cols\n        )\n        \n        # Merge original data\n        res = pd.merge(all_combinations, df, on=cols, how='left')\n        \n        # Fill missing values\n        if fill:\n            res.fi", "score": 0.9731, "script_id": "auto"}

## Edit Examples
(none)

---
id: vctrs.vec-fill-missing
package: vctrs
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# vctrs.vec-fill-missing

## Guidance
Translate R `vec_fill_missing` (FunctionCall from vctrs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "c81ad6c1", "r_snippet": "vec_cast(c(1.5, 2), integer())", "py_snippet": "try:\n    # np.array([1.5, 2], dtype=int) acts as the equivalent to vec_cast to integer\n    np.array([1.5, 2], dtype=int)\nexcept Exception as e:\n    print(e)", "score": 1.0, "script_id": "auto"}
- {"r_hash": "3aaba6c2", "r_snippet": "vec_fill_missing(x, direction = \"down\")", "py_snippet": "def vec_fill_missing(x, direction=\"down\", max_fill=None):\n    if isinstance(x, pd.DataFrame):\n        # Data frames are filled rowwise. Rows are only considered missing\n        # if all elements of that row are missing.\n        mask = x.isna().all(axis=1)\n        if not mask.any():\n            return x\n        \n        # Create a helper series to track the \"row-missing\" status\n        # We effectively treat the row as a single unit.\n        # To implement this in pandas, we can find non-missing rows\n        # and use them to fill the missing ones.\n        \n        # We can use a temporary colu", "score": 0.8382, "script_id": "auto"}

## Edit Examples
(none)

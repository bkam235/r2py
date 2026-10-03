---
id: sparsevctrs.sparse-replace-na
package: sparsevctrs
confidence: tentative
seed: true
created: 2026-09-24
last_review: 2026-09-24
tie_count: 0
---

# sparsevctrs.sparse-replace-na

## Guidance
Translate R `sparse_replace_na` (FunctionCall from sparsevctrs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "054f7cfe", "r_snippet": "sparse_replace_na(\n  sparse_double(c(10, NA, 11), c(1, 5, 10), 10),\n  5\n)", "py_snippet": "def sparse_replace_na(x, replace):\n    default = sparse_default(x)\n    values = sparse_values(x)\n    positions = sparse_positions(x)\n    \n    if len(values) == 0:\n        return x\n    \n    # Use pandas.isna to handle various NA types (np.nan, None, etc.)\n    mask_na = pd.isna(values)\n    \n    if replace == default:\n        # Remove elements that are NA\n        new_values = values[~mask_na]\n        new_positions = positions[~mask_na]\n    else:\n        # Replace NA values with the replace value\n        new_values = values.copy()\n        new_values[mask_na] = replace\n        new_positions = positions\n        \n    # Determine the constructor based on the type of values\n    if np.issubdtype(new_values.dtype, np.integer) or (len(new_values) > 0 and isinstance(new_values[0], (int, np.integer))):\n        return sparse_integer(new_values, new_positions, x.length, default)\n    elif np.issubdtype(new_values.dtype, np.floating) or (len(new_values) > 0 and isinstance(new_values[0], (float, np.floating))):\n        return sparse_double(new_values, new_positions, x.length, default)\n    else:\n        return sparse_character(new_values, new_positions, x.length, default)\n\n# Example 1\n\nres1 = sparse_replace_na(\n    sparse_double([10, np.nan, 11], [1, 5, 10], 10),\n    5\n)\nprint(res1)\n\n# Example 2", "score": 1.0, "script_id": "sparsevctrs__rd_example__sparse_replace_na_Rd", "n_calls": 0}

## Edit Examples
(none)

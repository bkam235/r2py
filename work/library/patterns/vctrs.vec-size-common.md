---
id: vctrs.vec-size-common
package: vctrs
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# vctrs.vec-size-common

## Guidance
Translate R `vec_size_common` (FunctionCall from vctrs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "ab370b3c", "r_snippet": "vec_size_common(1:3, 1:3, 1:3)", "py_snippet": "def vec_size_common(*args):\n    # In R's vctrs, vec_size_common returns the common size if all \n    # are the same, or 1 if they differ (following R's recycling rules)\n    # except if any are length 0, it returns 0.\n    sizes = [len(x) if hasattr(x, '__len__') else 1 for x in args]\n    \n    if any(s == 0 for s in sizes):\n        return 0\n    \n    if all(s == sizes[0] for s in sizes):\n        return sizes[0]\n    \n    return 1\n\n# vec_size_common(1:3, 1:3, 1:3)\n\nprint(vec_size_common(list(range(1, 4)), list(range(1, 4)), list(range(1, 4))))\n\n# vec_size_common(1:10, 1)", "score": 1.0, "script_id": "auto"}
- {"r_hash": "a0e24653", "r_snippet": "vec_ptype_show(\n      array(1, c(0, 1)), \n      array(1, c(0, 2))\n    )", "py_snippet": "def get_vec_ptype_full(x):\n    \"\"\"\n    Mimics vec_ptype_full.default and vec_ptype_shape.\n    R's array(1, c(0, 1)) is a double array. \n    Shape (0, 1) in R is denoted as <double[,1]>.\n    \"\"\"\n    # Check if it is a numpy array\n    if isinstance(x, np.ndarray):\n        dtype_str = \"double\" if x.dtype == np.float64 or x.dtype == np.int64 or x.dtype == np.int32 else str(x.dtype)\n        # R arrays: the first dimension is often omitted in the [,] notation if it's the length/rows\n        # array(1, c(0, 1)) -> <double[,1]>\n        # array(1, c(0, 3, 4)) -> <double[,3,4]>\n        shape = x.shape\n ", "score": 1.0, "script_id": "auto"}
- {"r_hash": "bd53a93f", "r_snippet": "vec_rank(x, ties = \"min\")", "py_snippet": "def vec_rank(x, ties=\"min\", incomplete=\"rank\", direction=\"asc\", na_value=\"largest\", nan_distinct=False):\n    if isinstance(x, pd.DataFrame):\n        # Lexicographical rank for data frames\n        # R's vec_rank(df) ranks rows based on columns in order\n        # We use pandas' rank with a trick: sort by all columns, then rank the resulting sequence\n        sorted_df = x.sort_values(by=x.columns.tolist())\n        \n        # To implement 'min' rank on lexicographical order:\n        # We identify groups of identical rows\n        # In this specific case, the R example uses default ties=\"min\"\n      ", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

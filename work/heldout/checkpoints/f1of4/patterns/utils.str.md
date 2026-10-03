---
id: utils.str
package: utils
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# utils.str

## Guidance
Translate R `str` (FunctionCall from utils) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "9a1df3fc", "r_snippet": "str(\n  sparse_logical(c(TRUE, NA, TRUE), c(2, 5, 10), 1000000000)\n)", "py_snippet": "def str_obj(obj):\n    \"\"\"Equivalent to R's str() for the SparseLogical object.\"\"\"\n    if isinstance(obj, SparseLogical):\n        dense = obj.to_dense() if obj.length < 100 else None\n        if dense is not None:\n            # For small vectors, str() shows a few values\n            vals = []\n            for v in dense[:6]:\n                vals.append(\"NA\" if pd.isna(v) else str(v).upper())\n            print(f\"logi [{1}:{obj.length}] {' '.join(vals)} ...\")\n        else:\n            # For huge vectors, it shows the range and the first few values\n            # R output: logi [1:1000000000] FALSE TRUE FALSE FALSE NA FALSE ...\n            # We compute the first 6 elements of the sparse vector\n            res = np.full(6, obj.default, dtype=object)\n            for v, p in zip(obj.values, obj.positions):\n                if 1 <= p <= 6:\n                    res[p-1] = v\n            vals = []\n            for v in res:\n                vals.append(\"NA\" if pd.isna(v) else str(v).upper())\n            print(f\"logi [{1}:{obj.length}] {' '.join(vals)} ...\")\n    else:\n        print(repr(obj))\n\n# Example 1: sparse_logical(logical(), integer(), 10)\n\nres3 = sparse_logical([True, np.nan, True], [2, 5, 10], 1000000000)\nstr_obj(res3)", "score": 1.0, "script_id": "sparsevctrs__rd_example__sparse_logical_Rd", "n_calls": 1}

## Edit Examples
- {"failure_class": "side_effects", "old_code": "def str_obj(object):\n    \"\"\"Equivalent to R's str() for the SparseLogical object.\"\"\"\n    print(repr(object))\n\n# Example 1: sparse_logical(logical(), integer(), 10)\nres1 = sparse_logical([], [], 10)\nprint(res1)\n\n# Example 2: sparse_logical(c(TRUE, NA, TRUE), c(2, 5, 10), 10)\n\nres3 = sparse_logical([True, np.nan, True], [2, 5, 10], 1000000000)\nstr_obj(res3)", "new_code": "def str_obj(obj):\n    \"\"\"Equivalent to R's str() for the SparseLogical object.\"\"\"\n    if isinstance(obj, SparseLogical):\n        dense = obj.to_dense() if obj.length < 100 else None\n        if dense is not None:\n            # For small vectors, str() shows a few values\n            vals = []\n            for v in dense[:6]:\n                vals.append(\"NA\" if pd.isna(v) else str(v).upper())\n            print(f\"logi [{1}:{obj.length}] {' '.join(vals)} ...\")\n        else:\n            # For huge vectors, it shows the range and the first few values\n            # R output: logi [1:1000000000] FALSE TRUE FALSE FALSE NA FALSE ...\n            # We compute the first 6 elements of the sparse vector\n            res = np.full(6, obj.default, dtype=object)\n            for v, p in zip(obj.values, obj.positions):\n                if 1 <= p <= 6:\n                    res[p-1] = v\n            vals = []\n            for v in res:\n                vals.append(\"NA\" if pd.isna(v) else str(v).upper())\n            print(f\"logi [{1}:{obj.length}] {' '.join(vals)} ...\")\n    else:\n        print(repr(obj))\n\n# Example 1: sparse_logical(logical(), integer(), 10)\n\nres3 = sparse_logical([True, np.nan, True], [2, 5, 10], 1000000000)\nstr_obj(res3)", "score_delta": 0.3444, "script_id": "sparsevctrs__rd_example__sparse_logical_Rd", "r_snippet": "str(\n  sparse_logical(c(TRUE, NA, TRUE), c(2, 5, 10), 1000000000)\n)", "functions": ["utils::str"]}

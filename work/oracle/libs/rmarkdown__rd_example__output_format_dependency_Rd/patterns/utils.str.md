---
id: utils.str
package: utils
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# utils.str

## Guidance
Translate R `str` from utils to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "6ea9c27f", "r_snippet": "str(vars)", "py_snippet": "def str_obj(obj):\n    \"\"\"Equivalent to R's str() for data frames.\"\"\"\n    if isinstance(obj, pd.DataFrame):\n        print(f\"'data.frame':\\t{obj.shape[0]} obs. of  {obj.shape[1]} variables:\")\n        for col in obj.columns:\n            dtype = obj[col].dtype\n            # Map pandas dtype to R-style labels\n            if pd.api.types.is_integer_dtype(dtype):\n                type_str = \"int\"\n            elif pd.api.types.is_float_dtype(dtype):\n                type_str = \"num\"\n            elif pd.api.types.is_object_dtype(dtype):\n                type_str = \"chr\"\n            else:\n                type_str = str(dtype)\n            \n            # R's str() typically shows a few values\n            vals = obj[col].head(4).tolist()\n            # Format values: strings get quotes, numbers don't\n            formatted_vals = []\n            for v in vals:\n                if isinstance(v, str):\n                    formatted_vals.append(f'\"{v}\"')\n                else:\n                    formatted_vals.append(str(v))\n            \n            vals_str = \" \".join(formatted_vals)\n            print(f\" $ {col} : {type_str}  {vals_str}\")\n    else:\nfor i in range(len(vars)):", "score": 1.0, "script_id": "reshape2__rd_example__colsplit_Rd.R", "n_calls": 1}
- {"r_hash": "9a1df3fc", "r_snippet": "str(\n  sparse_logical(c(TRUE, NA, TRUE), c(2, 5, 10), 1000000000)\n)", "py_snippet": "def str_obj(obj):\n    \"\"\"Equivalent to R's str() for the SparseLogical object.\"\"\"\n    if isinstance(obj, SparseLogical):\n        dense = obj.to_dense() if obj.length < 100 else None\n        if dense is not None:\n            # For small vectors, str() shows a few values\n            vals = []\n            for v in dense[:6]:\n                vals.append(\"NA\" if pd.isna(v) else str(v).upper())\n            print(f\"logi [{1}:{obj.length}] {' '.join(vals)} ...\")\n        else:\n            # For huge vectors, it shows the range and the first few values\n            # R output: logi [1:1000000000] FALSE TRUE FALSE FALSE NA FALSE ...\n            # We compute the first 6 elements of the sparse vector\n            res = np.full(6, obj.default, dtype=object)\n            for v, p in zip(obj.values, obj.positions):\n                if 1 <= p <= 6:\n                    res[p-1] = v\n            vals = []\n            for v in res:\n                vals.append(\"NA\" if pd.isna(v) else str(v).upper())\n            print(f\"logi [{1}:{obj.length}] {' '.join(vals)} ...\")\n    else:\n        print(repr(obj))\n\nprint(res2)", "score": 1.0, "script_id": "sparsevctrs__rd_example__sparse_logical_Rd.R", "n_calls": 1}

## Edit Examples
(none)

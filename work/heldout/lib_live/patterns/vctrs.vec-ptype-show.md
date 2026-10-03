---
id: vctrs.vec-ptype-show
package: vctrs
confidence: tentative
seed: true
created: 2026-09-22
last_review: 2026-09-22
tie_count: 0
---

# vctrs.vec-ptype-show

## Guidance
Translate R `vec_ptype_show` (FunctionCall from vctrs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "87309418", "r_snippet": "vec_ptype_show(\n  data.frame(x = FALSE), \n  data.frame(x = 1L),\n  data.frame(x = 2.5)\n)", "py_snippet": "def vec_ptype_full(x):\n    \"\"\"\n    Approximates vctrs::vec_ptype_full by describing the structure and types\n    of the provided object.\n    \"\"\"\n    if isinstance(x, pd.DataFrame):\n        if x.empty and len(x.columns) == 0:\n            return \"data.frame<>\"\n        \n        if len(x.columns) == 1:\n            col_name = x.columns[0]\n            return f\"data.frame<{col_name}:{vec_ptype_full(x[col_name])}>\"\n        \n        col_types = []\n        for col_name in x.columns:\n            ptype = vec_ptype_full(x[col_name])\n            col_types.append(f\"  {col_name}: {ptype}\")\n        \n        return \"data.frame<\\n\" + \"\\n\".join(col_types) + \"\\n>\"\n    \n    elif isinstance(x, pd.Series):\n        dtype = x.dtype\n        if pd.api.types.is_bool_dtype(dtype):\n            return \"logical\"\n        elif pd.api.types.is_integer_dtype(dtype):\n            return \"integer\"\n        elif pd.api.types.is_float_dtype(dtype):\n            return \"double\"\n        elif pd.api.types.is_object_dtype(dtype):\n            return \"character\"\n        return str(dtype)\n    \n    return str(type(x).__name__)\n\ndef vec_ptype2(x_type, y_type):\n    \"\"\"\n    Approximates vctrs::vec_ptype2.\n    Handles types as strings since vec_ptype_show uses in_types = map(args, vec_ptype).\n    \"\"\"\n    # Handle data.frame types\n    if \"data.frame\" in x_type and \"data.frame\" in y_type:\n        # Extract internals: data.frame<x:logical> -> x:logical\n        def get_internals(t):\n            return t[t.find('<')+1 : t.rfind('>')]\n        \n        x_int = get_internals(x_type)\n        y_int = get_internals(y_type)\n        \n        # For this specific case, we assume columns are the same\n        # Split by ':' if it's a simple single column DF\n        if ':' in x_int and ':' in y_int:\n            x_col, x_t = x_int.split(':', 1)\n            y_col, y_t = y_int.split(':', 1)\n            res_t = vec_ptype2(x_t, y_t)\n            return f\"data.frame<{x_col}:{res_t}>\"\n        \n        return x_type # Fallback\n        \n# ...", "score": 0.9899, "script_id": "vctrs__vignette__type-size_s17", "n_calls": 1}

## Edit Examples
(none)

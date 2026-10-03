---
id: dplyr.glimpse
package: dplyr
confidence: tentative
seed: true
created: 2026-09-22
last_review: 2026-09-22
tie_count: 0
---

# dplyr.glimpse

## Guidance
Translate R `glimpse` (FunctionCall from dplyr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "fddfca61", "r_snippet": "glimpse(mtcars)", "py_snippet": "def glimpse(x, width=None):\n    df = pd.DataFrame(x)\n    rows, cols = df.shape\n    print(f\"Rows: {rows}\")\n    print(f\"Columns: {cols}\")\n    \n    for col in df.columns:\n        dtype = df[col].dtype\n        # Map numpy/pandas dtypes to R-like labels\n        if pd.api.types.is_float_dtype(dtype):\n            type_label = \"<dbl>\"\n        elif pd.api.types.is_integer_dtype(dtype):\n            type_label = \"<int>\"\n        elif pd.api.types.is_bool_dtype(dtype):\n            type_label = \"<lgl>\"\n        else:\n            type_label = \"<chr>\"\n        \n        # Get values and format as a comma-separated string\n        vals = df[col].values\n        val_str = \", \".join(map(str, vals[:10]))\n        if len(vals) > 10:\n            val_str += \", ...\"\n            \n        print(f\"$ {col} {type_label} {val_str}\")\n    \n    return x\n\nglimpse(mtcars)\n\n# mtcars |> glimpse() |> select(1:3)\n# In R, glimpse returns the object invisibly.", "score": 0.9333, "script_id": "dplyr__rd_example__glimpse_Rd", "n_calls": 0}

## Edit Examples
(none)

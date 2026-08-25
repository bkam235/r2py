---
id: dplyr.filter
package: dplyr
confidence: tentative
seed: true
created: 2026-07-06
last_review: 2026-07-06
tie_count: 0
---

# dplyr.filter

## Guidance
Translate R `filter` (FunctionCall from dplyr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "00475275", "r_snippet": "arrange(wrong, year)", "py_snippet": "print(wrong.sort_values('year').reset_index(drop=True))\n\n# Right way: lag with ordering by year", "score": 0.9564, "script_id": "auto"}
- {"r_hash": "5e9acb5c", "r_snippet": "  select(1:3)", "py_snippet": "result = res.iloc[:, 0:3]\n# Note: The R code doesn't print the result of the pipeline, \n# but since the script ends with another glimpse, we just compute it.", "score": 0.9333, "script_id": "auto"}
- {"r_hash": "fddfca61", "r_snippet": "glimpse(mtcars)", "py_snippet": "def glimpse(df):\n    \"\"\"Mimics dplyr::glimpse output.\"\"\"\n    rows = len(df)\n    cols = len(df.columns)\n    print(f\"Rows: {rows}\")\n    print(f\"Columns: {cols}\")\n    \n    for col in df.columns:\n        dtype = df[col].dtype\n        # Map numpy/pandas dtypes to R-like glimpses\n        if \"float\" in str(dtype):\n            r_type = \"<dbl>\"\n        elif \"int\" in str(dtype):\n            r_type = \"<int>\"\n        elif \"object\" in str(dtype):\n            r_type = \"<chr>\"\n        else:\n            r_type = f\"<{dtype}>\"\n            \n        # Get first few values\n        vals = df[col].head(10).tolist()\n", "score": 0.9333, "script_id": "auto"}

## Edit Examples
(none)

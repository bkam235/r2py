---
id: data.table.setkey
package: data.table
confidence: tentative
seed: true
created: 2026-08-21
last_review: 2026-08-21
tie_count: 0
---

# data.table.setkey

## Guidance
Translate R `setkey` (FunctionCall from data.table) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "96241957", "r_snippet": "setkey(DT,B)", "py_snippet": "DT = DT.sort_values('B').reset_index(drop=True)\nDT.attrs['key'] = ['B']\n\n# Entity: tables", "score": 1.0, "script_id": "auto"}
- {"r_hash": "aa3c4e0f", "r_snippet": "substitute2(   # mimicking base R's \"substitute\" using \"I\"\n  rank(input, ties.method = ties),\n  env = I(list(input = as.name(\"Sepal.Width\"), ties = \"first\"))\n)", "py_snippet": "def substitute2(expr_str, env=None):\n    \"\"\"\n    Mimics substitute2, which uses I() to determine if a value is treated as a literal.\n    \"\"\"\n    if env is None:\n        return expr_str\n    \n    # In substitute2, if the env itself is wrapped in I(), \n    # or if elements are wrapped in I(), behavior changes.\n    \n    # Handle the case where the whole env is I(list(...))\n    actual_env = env\n    if isinstance(env, AsIs):\n        actual_env = env.value\n    \n    result = expr_str\n    import re\n    for key, val in actual_env.items():\n        pattern = r'\\b' + re.escape(key) + r'\\b'\n        \n       ", "score": 0.9507, "script_id": "auto"}

## Edit Examples
(none)

---
id: dbplyr.build-sql
package: dbplyr
confidence: tentative
seed: true
created: 2026-09-05
last_review: 2026-09-05
tie_count: 0
---

# dbplyr.build-sql

## Guidance
Translate R `build_sql` (FunctionCall from dbplyr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "ebdfcd3e", "r_snippet": "sql_expr(f(x + 1), con = con)", "py_snippet": "def replace_expr(x, con=None):\n    if x is None:\n        return \"NULL\"\n    \n    # Handle ident object\n    if isinstance(x, dict) and x.get(\"type\") == \"ident\":\n        return f\"`{x['value']}`\"\n    \n    # Handle atomic types (strings, numbers)\n    if isinstance(x, (str, int, float)):\n        if isinstance(x, float) or (isinstance(x, int) and False): # Simplified\n            return str(float(x))\n        if isinstance(x, int):\n            # In dbplyr, constants are often cast to floats in SQL\n            return f\"{float(x)}\"\n        return f\"'{x}'\" if isinstance(x, str) and not x.startswith(\"`\") e", "score": 1.0, "script_id": "auto"}
- {"r_hash": "4bec2ac7", "r_snippet": "sql_call2(\"+\", quote(x), 1, con = con)", "py_snippet": "def sql_call2(fn, *args, con=None):\n    \"\"\"Mimics sql_call2 which constructs a SQL call.\"\"\"\n    expr_tuple = (fn, *args)\n    res = replace_expr(expr_tuple, con=con)\n    return sql(res)\n\n# Helper for R's %as% and %::%\n\nprint(sql_call2(\"+\", 'x', 1, con=con))\n\n# sql_call2(\"+\", \"x\", 1, con = con)\n# In this case, \"x\" is a string literal", "score": 1.0, "script_id": "auto"}
- {"r_hash": "20392dbe", "r_snippet": "build_sql(\"SELECT * FROM TABLE\", con = con)", "py_snippet": "def build_sql(*args):\n    # Simplified substitute for build_sql: joins arguments into a string\n    # In real scenarios, one would use parameterized queries to prevent injection\n    return \"\".join(str(arg) for arg in args)\n\n# Example 1\n\nprint(build_sql(\"SELECT * FROM TABLE\"))\n\n# Example 2", "score": 0.9318, "script_id": "auto"}

## Edit Examples
(none)

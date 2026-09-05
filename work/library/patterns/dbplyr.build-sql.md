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
- {"r_hash": "20392dbe", "r_snippet": "build_sql(\"SELECT * FROM TABLE\", con = con)", "py_snippet": "def build_sql(*args):\n    # Simplified substitute for build_sql: joins arguments into a string\n    # In real scenarios, one would use parameterized queries to prevent injection\n    return \"\".join(str(arg) for arg in args)\n\n# Example 1\n\nprint(build_sql(\"SELECT * FROM TABLE\"))\n\n# Example 2", "score": 0.9318, "script_id": "auto"}

## Edit Examples
(none)

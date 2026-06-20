---
id: xfun.cache-rds-return-value
package: 
confidence: tentative
seed: false
created: 2026-06-15
last_review: 2026-06-15
tie_count: 0
---

# xfun.cache-rds-return-value

## Guidance
When translating R's xfun::cache_rds() with an expression block, the Python equivalent must return the final value of the expression. In R, the last evaluated expression in a block is returned; ensure the Python function returns the same value (e.g., a list for R sequences).

## Evidence
- 34ab01c45818 → score 0.250 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "env", "old_code": "def compute_func():\n    \"\"\"Placeholder function that takes one second.\"\"\"\n    time.sleep(1)", "new_code": "def compute_func():\n    \"\"\"Placeholder function that takes one second.\"\"\"\n    time.sleep(1)\n    return list(range(1, 11))", "score_delta": 0.2503, "script_id": "34ab01c45818"}

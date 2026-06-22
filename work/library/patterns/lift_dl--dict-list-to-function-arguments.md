---
id: lift_dl--dict-list-to-function-arguments
package: purrr
confidence: tentative
seed: true
created: 2026-06-20
last_review: 2026-06-20
tie_count: 0
---

# lift_dl--dict-list-to-function-arguments

## Guidance
When lifting a function with `lift_dl()`, the returned wrapper should accept a dict or list and expand its contents as function arguments. If a dict has an 'x' key, use it as the first positional argument; merge remaining keys as kwargs after converting dot notation to underscores.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "ebdeea84", "r_snippet": "suppressPackageStartupMessages(library(purrr))", "py_snippet": "warnings.filterwarnings('ignore')", "score": 1.0, "script_id": "21f4191f6dbb"}

## Edit Examples
(none)

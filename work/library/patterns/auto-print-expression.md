---
id: auto-print-expression
package: 
confidence: tentative
seed: false
created: 2026-06-13
last_review: 2026-06-13
tie_count: 0
---

# auto-print-expression

## Guidance
In R, bare expressions at the top level are auto-printed to stdout. In Python, function calls do not auto-print unless wrapped in print(). When an R expression is meant to be auto-printed, capture its result and explicitly print it to match R's behavior.

## Evidence
- d42c7e223bcd → score 0.183 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "graycol(10)", "new_code": "result = graycol(10)\nprint(result)", "score_delta": 0.1833, "script_id": "d42c7e223bcd"}

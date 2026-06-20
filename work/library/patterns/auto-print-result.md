---
id: auto-print-result
package: 
confidence: tentative
seed: false
created: 2026-06-11
last_review: 2026-06-11
tie_count: 0
---

# auto-print-result

## Guidance
In R, top-level expressions auto-print their results to stdout. In Python, you must explicitly call print() to achieve the same output behavior. Wrap function calls that should display results with print().

## Evidence
- d42c7e223bcd → score 0.183 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "graycol(10)", "new_code": "print(graycol(10))", "score_delta": 0.1833, "script_id": "d42c7e223bcd"}

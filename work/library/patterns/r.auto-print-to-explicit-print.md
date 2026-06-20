---
id: r.auto-print-to-explicit-print
package: shape
confidence: tentative
seed: false
created: 2026-06-09
last_review: 2026-06-09
tie_count: 0
---

# r.auto-print-to-explicit-print

## Guidance
In R, top-level expressions are auto-printed to stdout. In Python, use explicit print() to achieve the same behavior when translating bare function calls that should display their return value.

## Evidence
- d42c7e223bcd → score 0.084 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "graycol(10)", "new_code": "print(graycol(10))", "score_delta": 0.0835, "script_id": "d42c7e223bcd"}

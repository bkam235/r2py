---
id: r.auto-print-to-stdout
package: 
confidence: tentative
seed: false
created: 2026-06-08
last_review: 2026-06-08
tie_count: 0
---

# r.auto-print-to-stdout

## Guidance
R automatically prints the result of the last expression in a block to stdout; Python requires an explicit print() call to achieve the same behavior.

## Evidence
- dd2e0ea0b08b → score 0.051 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "graycol_impl(10)", "new_code": "print(graycol_impl(10))", "score_delta": 0.0511, "script_id": "dd2e0ea0b08b"}

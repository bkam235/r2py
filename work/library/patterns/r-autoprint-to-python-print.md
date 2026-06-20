---
id: r-autoprint-to-python-print
package: 
confidence: tentative
seed: false
created: 2026-06-07
last_review: 2026-06-07
tie_count: 0
---

# r-autoprint-to-python-print

## Guidance
In R, top-level function calls that return values auto-print to stdout. In Python, explicit print() calls are required to produce stdout output. When translating R code that calls a function for its printed side effect, wrap or follow the call with print() to match the behavior.

## Evidence
- dd2e0ea0b08b → score 0.051 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "graycol_result = [f'#{int(255*i/9):02x}{int(255*i/9):02x}{int(255*i/9):02x}' for i in range(10)]", "new_code": "graycol_result = [f'#{int(255*i/9):02x}{int(255*i/9):02x}{int(255*i/9):02x}' for i in range(10)]\nprint(graycol_result)", "score_delta": 0.0511, "script_id": "dd2e0ea0b08b"}

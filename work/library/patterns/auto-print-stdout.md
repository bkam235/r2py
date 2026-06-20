---
id: auto-print-stdout
package: 
confidence: tentative
seed: false
created: 2026-06-07
last_review: 2026-06-07
tie_count: 0
---

# auto-print-stdout

## Guidance
In R, bare expressions at the top level are auto-printed to stdout. In Python, you must explicitly call print() to output results. When translating an R expression that produces output, wrap it with print() to match the R behavior.

## Evidence
- dd2e0ea0b08b → score 0.051 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "graycol_result = [f'#{int(val*255):02x}{int(val*255):02x}{int(val*255):02x}' \n                  for val in [i/(10-1) for i in range(10)]]", "new_code": "print([f'#{int(val*255):02x}{int(val*255):02x}{int(val*255):02x}' \n       for val in [i/(10-1) for i in range(10)]])", "score_delta": 0.0511, "script_id": "dd2e0ea0b08b"}

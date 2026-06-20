---
id: param-name-underscore
package: 
confidence: tentative
seed: false
created: 2026-06-18
last_review: 2026-06-18
tie_count: 0
---

# param-name-underscore

## Guidance
When translating R function parameters with dots (e.g., length.out) to Python, use underscores (length_out). Ensure all call sites use the Python parameter names, not R's dot notation.

## Evidence
- ca1440d6104b → score 0.170 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "chunk(bytes(10000000), length=3)", "new_code": "chunk(bytes(10000000), length_out=3)", "score_delta": 0.1699, "script_id": "ca1440d6104b"}

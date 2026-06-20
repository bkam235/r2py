---
id: chunk.auto-print-result
package: 
confidence: tentative
seed: false
created: 2026-06-17
last_review: 2026-06-17
tie_count: 0
---

# chunk.auto-print-result

## Guidance
R auto-prints function results at the top level; Python requires explicit print(). For chunk() calls that return named lists, capture the result and iterate over items printing the key (wrapped in $``) and the repr() of the value.

## Evidence
- ca1440d6104b → score 0.115 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)

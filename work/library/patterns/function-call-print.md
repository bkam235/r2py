---
id: function-call-print
package: 
confidence: tentative
seed: false
created: 2026-06-11
last_review: 2026-06-11
tie_count: 0
---

# function-call-print

## Guidance
When an R function call appears at the top level (not assigned to a variable), it typically prints its return value. In Python, wrap the function call with print() to reproduce this behavior and ensure stdout output is generated.

## Evidence
- d42c7e223bcd → score 0.287 (path: exact, variable: )

## Contradictions
- d42c7e223bcd/: score regressed to 0.133

## Translation Examples
(none)

## Edit Examples
(none)

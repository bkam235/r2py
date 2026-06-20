---
id: missing-function-call
package: 
confidence: tentative
seed: false
created: 2026-06-18
last_review: 2026-06-18
tie_count: 0
---

# missing-function-call

## Guidance
When an R script calls a function defined earlier, the Python translation must include the actual function call statement. If the call produces output through print statements within the function, ensure the call is executed at module level so the output is generated.

## Evidence
- ca1440d6104b → score 0.194 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)

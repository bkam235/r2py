---
id: r-function-with-dual-mode--data-vs.-specification
package: bit
confidence: tentative
seed: false
created: 2026-06-29
last_review: 2026-06-29
tie_count: 0
---

# r-function-with-dual-mode--data-vs.-specification

## Guidance
When an R function can accept either data as first argument OR chunk specification parameters, use a union of parameter modes in Python. Check if x is provided and is actual data; otherwise, treat positional/keyword arguments as specification parameters that delegate to a helper function.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)

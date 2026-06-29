---
id: backward-compatible-positional-argument-handling
package: bit
confidence: tentative
seed: false
created: 2026-06-29
last_review: 2026-06-29
tie_count: 0
---

# backward-compatible-positional-argument-handling

## Guidance
For R functions that support both old positional syntax (e.g., chunk(1, 100, 10)) and new named syntax (e.g., chunk(from=1, to=100, by=10)), explicitly handle positional arguments in the Python signature and document which mode applies based on argument types and counts.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)

---
id: as.logical---coercion
package: base
confidence: tentative
seed: false
created: 2026-06-29
last_review: 2026-06-29
tie_count: 0
---

# as.logical---coercion

## Guidance
Translate R's as.logical(numeric_vector) to Python using a list comprehension with bool(): [bool(val) for val in vector]. Non-zero values become TRUE, zero becomes FALSE.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)

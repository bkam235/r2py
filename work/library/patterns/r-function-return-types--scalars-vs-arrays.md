---
id: r-function-return-types--scalars-vs-arrays
package: broom
confidence: tentative
seed: false
created: 2026-06-23
last_review: 2026-06-23
tie_count: 0
---

# r-function-return-types--scalars-vs-arrays

## Guidance
If an R function returns a single-value vector for a default parameter (e.g., max_lag=1), the Python equivalent should return a scalar instead of a single-element array to ensure compatibility with downstream dataframes.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)

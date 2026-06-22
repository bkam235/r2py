---
id: r-scalar-return--max_lag-1
package: broom
confidence: tentative
seed: false
created: 2026-06-22
last_review: 2026-06-22
tie_count: 0
---

# r-scalar-return--max_lag-1

## Guidance
When translating R functions that return a vector for multiple lags but a scalar for a single lag, use conditional indexing (e.g., `vals[0] if max_lag == 1 else vals`) to match the expected return type.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)

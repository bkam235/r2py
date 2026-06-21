---
id: dplyr--lag-with-order_by
package: dplyr
confidence: tentative
seed: false
created: 2026-06-21
last_review: 2026-06-21
tie_count: 0
---

# dplyr--lag-with-order_by

## Guidance
To implement `lag(x, order_by = y)`, sort the data by `y`, apply `.shift(n)`, and then re-align the results to the original index of `x`.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)

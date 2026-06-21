---
id: r-vector-to-python-list-dataframe
package: prodlim
confidence: tentative
seed: false
created: 2026-06-21
last_review: 2026-06-21
tie_count: 0
---

# r-vector-to-python-list-dataframe

## Guidance
When a vector is used as the first argument in a row-matching context, treat it as a single-row DataFrame by wrapping the list in another list: `pd.DataFrame([x])`.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)

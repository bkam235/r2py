---
id: vec_fill_missing--dataframe
package: vctrs
confidence: tentative
seed: false
created: 2026-06-21
last_review: 2026-06-21
tie_count: 0
---

# vec_fill_missing--dataframe

## Guidance
When applying row-filling to a DataFrame, R defines a row as 'missing' only if ALL elements in that row are NA; do not use standard pandas ffill/bfill which operates on a per-column basis.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)

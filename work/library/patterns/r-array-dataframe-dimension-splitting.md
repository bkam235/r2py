---
id: r-array-dataframe-dimension-splitting
package: plyr
confidence: tentative
seed: false
created: 2026-06-21
last_review: 2026-06-21
tie_count: 0
---

# r-array-dataframe-dimension-splitting

## Guidance
R's `splitter_a(x, dim)` uses 1-indexed dimensions; in Python, convert to 0-indexed and handle differently for DataFrames (split rows/columns) versus NumPy arrays (use array slicing along axes).

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)

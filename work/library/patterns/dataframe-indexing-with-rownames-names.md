---
id: dataframe-indexing-with-rownames-names
package: dplyr
confidence: tentative
seed: false
created: 2026-06-21
last_review: 2026-06-21
tie_count: 0
---

# dataframe-indexing-with-rownames-names

## Guidance
R's `df[rownames(df1), names(df1)]` should be translated to Python's `df.loc[df1.index, df1.columns]` to reorder a DataFrame to match the row and column sequence of another.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)

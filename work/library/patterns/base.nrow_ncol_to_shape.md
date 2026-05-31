---
id: base.nrow_ncol_to_shape
package: base
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
---

# base.nrow_ncol_to_shape

## Guidance
`nrow(df)` → `len(df)` or `df.shape[0]`. `ncol(df)` → `len(df.columns)` or
`df.shape[1]`. `dim(df)` → `df.shape` (returns a tuple). `length(x)` → `len(x)` for
lists/vectors; for DataFrames `len(x)` gives the number of columns (ncol equivalent) —
use `df.shape[0]` for nrow. `NROW(x)` / `NCOL(x)` → same as nrow/ncol.

## Evidence
(none)

## Contradictions
(none)

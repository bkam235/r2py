---
id: base.na_to_none
package: base
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
---

# base.na_to_none

## Guidance
R `NA` → Python `None` in general scalar contexts. In pandas/numpy contexts use
`pd.NA` (integer/boolean NA) or `float("nan")` (numeric NA). `is.na(x)` →
`pd.isna(x)` or `x is None`. `NA_character_` / `NA_real_` / `NA_integer_` →
`None` when not in a DataFrame column; use the appropriate pandas NA type inside
DataFrames.

## Evidence
(none)

## Contradictions
(none)

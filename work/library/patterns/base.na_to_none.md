---
id: base.na_to_none
package: base
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
tie_count: 0
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

## Translation Examples
- {"r_hash": "1b785ce7", "r_snippet": "suppressPackageStartupMessages(library(bit))", "py_snippet": "warnings.filterwarnings('ignore')", "score": 1.0, "script_id": "0f2136d787dc"}
- {"r_hash": "9f4ae2da", "r_snippet": "suppressPackageStartupMessages(library(broom))", "py_snippet": "warnings.filterwarnings('ignore')", "score": 1.0, "script_id": "4e102aa60f9d"}

## Edit Examples
(none)

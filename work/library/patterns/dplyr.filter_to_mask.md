---
id: dplyr.filter_to_mask
package: dplyr
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
tie_count: 0
---

# dplyr.filter_to_mask

## Guidance
`dplyr::filter(df, condition)` → `df[condition]` or `df.query("condition_str")`.
For complex conditions, boolean indexing is clearest: `filter(df, x > 0 & y < 5)` →
`df[(df["x"] > 0) & (df["y"] < 5)]`. `filter(df, !is.na(x))` → `df[df["x"].notna()]`.
When using `.query()`, column names with spaces need backtick-quoting. Prefer boolean
indexing for clarity and verifier compatibility.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "d9d14ebe", "r_snippet": "suppressPackageStartupMessages(library(dplyr))", "py_snippet": "warnings.filterwarnings('ignore')", "score": 1.0, "script_id": "9c532ab9a0a0"}

## Edit Examples
(none)

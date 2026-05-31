---
id: dplyr.filter_to_mask
package: dplyr
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
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

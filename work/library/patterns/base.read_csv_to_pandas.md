---
id: base.read_csv_to_pandas
package: base
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
---

# base.read_csv_to_pandas

## Guidance
`read.csv("file.csv")` → `pd.read_csv("file.csv")`. R's default `stringsAsFactors`
behavior differs by version; Python read_csv does not produce categoricals by default —
add `.astype("category")` explicitly if needed. `read.csv(..., header=FALSE)` →
`pd.read_csv(..., header=None)`. `read.csv(..., sep="\t")` → `pd.read_csv(..., sep="\t")`
or `pd.read_table(...)`.

## Evidence
(none)

## Contradictions
(none)

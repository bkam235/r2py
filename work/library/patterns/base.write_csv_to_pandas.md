---
id: base.write_csv_to_pandas
package: base
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
---

# base.write_csv_to_pandas

## Guidance
`write.csv(df, "file.csv")` → `df.to_csv("file.csv")`. R's `write.csv` adds a row-name
column by default; suppress it in Python with `index=False`: `df.to_csv("file.csv",
index=False)`. `write.csv(df, "file.csv", row.names=FALSE)` → `df.to_csv("file.csv",
index=False)`. Use `sep=","` explicitly if the downstream reader expects a strict CSV.

## Evidence
(none)

## Contradictions
(none)

---
id: data.table.setkey
package: data.table
confidence: tentative
seed: true
created: 2026-08-21
last_review: 2026-08-21
tie_count: 0
---

# data.table.setkey

## Guidance
Translate R `setkey` (FunctionCall from data.table) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "96241957", "r_snippet": "setkey(DT,B)", "py_snippet": "DT = DT.sort_values('B').reset_index(drop=True)\nDT.attrs['key'] = ['B']\n\n# Entity: tables", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

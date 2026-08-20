---
id: forcats.lvls-revalue
package: forcats
confidence: tentative
seed: true
created: 2026-07-12
last_review: 2026-07-12
tie_count: 0
---

# forcats.lvls-revalue

## Guidance
Translate R `lvls_revalue` (FunctionCall from forcats) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "844f956c", "r_snippet": "lvls_revalue(f, c(\"apple\", \"banana\", \"carrot\"))", "py_snippet": "# lvls_revalue: rename levels\nf_revalued = f.rename_categories({\"a\": \"apple\", \"b\": \"banana\", \"c\": \"carrot\"})\nprint(f_revalued)", "score": 0.9095, "script_id": "auto"}

## Edit Examples
(none)

---
id: forcats.lvls-expand
package: forcats
confidence: tentative
seed: true
created: 2026-07-12
last_review: 2026-07-12
tie_count: 0
---

# forcats.lvls-expand

## Guidance
Translate R `lvls_expand` (FunctionCall from forcats) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "c64aeed0", "r_snippet": "lvls_expand(f, c(\"a\", \"b\", \"c\", \"d\"))", "py_snippet": "# lvls_expand: add new levels\nf_expanded = f.add_categories([\"d\"])\nprint(f_expanded)", "score": 0.8208, "script_id": "auto"}

## Edit Examples
(none)

---
id: forcats.lvls-reorder
package: forcats
confidence: tentative
seed: true
created: 2026-07-12
last_review: 2026-07-12
tie_count: 0
---

# forcats.lvls-reorder

## Guidance
Translate R `lvls_reorder` (FunctionCall from forcats) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "861642e0", "r_snippet": "lvls_reorder(f, 3:1)", "py_snippet": "# lvls_reorder: reorder levels in reverse order (3:1 means indices 2, 1, 0)\nf_reordered = f.reorder_categories(f.categories[[2, 1, 0]])\nprint(f_reordered)", "score": 0.8061, "script_id": "auto"}

## Edit Examples
(none)

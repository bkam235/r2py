---
id: recipes.prep
package: recipes
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# recipes.prep

## Guidance
Translate R `prep` (FunctionCall from recipes) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "ae5d7fda", "r_snippet": "  prep()", "py_snippet": "def prep(rec):\n    return rec.prep()\n\nrec1 = prep(rec1)", "score": 0.9333, "script_id": "auto"}

## Edit Examples
(none)

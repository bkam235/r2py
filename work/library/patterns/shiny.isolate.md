---
id: shiny.isolate
package: shiny
confidence: tentative
seed: true
created: 2026-09-14
last_review: 2026-09-14
tie_count: 0
---

# shiny.isolate

## Guidance
Translate R `isolate` (FunctionCall from shiny) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "50fdf44f", "r_snippet": "  isolate(x <- 2)", "py_snippet": "    with reactive.isolate():\n        x = 2", "score": 0.9667, "script_id": "auto"}

## Edit Examples
(none)

---
id: stringi.stri-startswith-fixed
package: stringi
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# stringi.stri-startswith-fixed

## Guidance
Translate R `stri_startswith_fixed` (FunctionCall from stringi) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "f577178a", "r_snippet": "stri_startswith_fixed(c('a1', 'a2', 'b3', 'a4', 'c5'), 'a')", "py_snippet": "# stri_startswith_fixed(c('a1', 'a2', 'b3', 'a4', 'c5'), 'a')\ndata = ['a1', 'a2', 'b3', 'a4', 'c5']\nprint([s.startswith('a') for s in data])", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

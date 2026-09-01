---
id: stringi.stri-startswith-coll
package: stringi
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# stringi.stri-startswith-coll

## Guidance
Translate R `stri_startswith_coll` (FunctionCall from stringi) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "b6fb0b3a", "r_snippet": "stri_startswith_coll(c('a1', 'A2', 'b3', 'A4', 'C5'), 'a', strength=1)", "py_snippet": "# stri_startswith_coll(c('a1', 'A2', 'b3', 'A4', 'C5'), 'a', strength=1)\n# strength=1 usually means case-insensitive\ndata_coll = ['a1', 'A2', 'b3', 'A4', 'C5']\nprint([s.lower().startswith('a') for s in data_coll])", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

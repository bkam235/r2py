---
id: dplyr.summarise
package: dplyr
confidence: tentative
seed: true
created: 2026-09-24
last_review: 2026-09-24
tie_count: 0
---

# dplyr.summarise

## Guidance
Translate R `summarise` (FunctionCall from dplyr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "cb24b082", "r_snippet": "  summarise(nrows = nrow(pick(everything())))", "py_snippet": "result = d.groupby('cyl').size().reset_index(name='nrows')", "score": 0.9333, "script_id": "dplyr__vignette__rowwise_s36", "n_calls": 1}

## Edit Examples
(none)

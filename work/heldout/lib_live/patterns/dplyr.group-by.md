---
id: dplyr.group-by
package: dplyr
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# dplyr.group-by

## Guidance
Translate R `group_by` (FunctionCall from dplyr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "9ae02bbd", "r_snippet": "      group_by(cyl) |>", "py_snippet": "grouped_mtcars = mtcars.groupby('cyl')\n\n# In R: summarise_mean(where(is.numeric))\n# We pass a dummy function or the logic inside our Python summarise_mean", "score": 0.9333, "script_id": "dplyr__vignette__programming_chunk10", "n_calls": 0}

## Edit Examples
(none)

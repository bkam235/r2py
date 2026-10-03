---
id: base.nrow
package: base
confidence: tentative
seed: true
created: 2026-09-24
last_review: 2026-09-24
tie_count: 0
---

# base.nrow

## Guidance
Translate R `nrow` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "cb24b082", "r_snippet": "  summarise(nrows = nrow(pick(everything())))", "py_snippet": "result = d.groupby('cyl').size().reset_index(name='nrows')", "score": 0.9333, "script_id": "dplyr__vignette__rowwise_s36", "n_calls": 1}

## Edit Examples
(none)

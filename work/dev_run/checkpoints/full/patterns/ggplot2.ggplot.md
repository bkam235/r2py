---
id: ggplot2.ggplot
package: ggplot2
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# ggplot2.ggplot

## Guidance
Translate R `ggplot` (FunctionCall from ggplot2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "ae7c854c", "r_snippet": "ggplot(mpg, aes(displ, hwy)) + ", "py_snippet": "plot = (\n    ggplot(d, aes(x='displ', y='hwy')) ", "score": 0.9333, "script_id": "ggplot2__vignette__extending-ggplot2_s16", "n_calls": 0}

## Edit Examples
(none)

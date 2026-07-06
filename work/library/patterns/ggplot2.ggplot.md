---
id: ggplot2.ggplot
package: ggplot2
confidence: tentative
seed: true
created: 2026-07-06
last_review: 2026-07-06
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
- {"r_hash": "9fa7ad5a", "r_snippet": "    ggplot(aes(long, lat, color = paste(year, name))) +", "py_snippet": "plot = (\n    ggplot(filtered_storms, aes(x='long', y='lat', color='color_label'))", "score": 0.9, "script_id": "auto"}

## Edit Examples
(none)

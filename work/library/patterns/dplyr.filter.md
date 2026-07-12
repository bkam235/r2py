---
id: dplyr.filter
package: dplyr
confidence: tentative
seed: true
created: 2026-07-06
last_review: 2026-07-06
tie_count: 0
---

# dplyr.filter

## Guidance
Translate R `filter` (FunctionCall from dplyr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "00475275", "r_snippet": "arrange(wrong, year)", "py_snippet": "print(wrong.sort_values('year').reset_index(drop=True))\n\n# Right way: lag with ordering by year", "score": 0.9564, "script_id": "auto"}
- {"r_hash": "82d5832d", "r_snippet": "    filter(year >= 2000) |>", "py_snippet": "filtered_storms = df_storms[df_storms['year'] >= 2000].copy()\n\n# In R: color = paste(year, name)\nfiltered_storms['color_label'] = filtered_storms['year'].astype(str) + \" \" + filtered_storms['name']", "score": 0.9, "script_id": "auto"}

## Edit Examples
(none)

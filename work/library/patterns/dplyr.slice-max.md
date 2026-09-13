---
id: dplyr.slice-max
package: dplyr
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# dplyr.slice-max

## Guidance
Translate R `slice_max` (FunctionCall from dplyr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "5cee929c", "r_snippet": "  mutate(rank = min_rank(height))", "py_snippet": "res1 = res1.assign(rank=res1['height'].rank(method='min').astype('Int64'))\nprint(res1)\n\n# Rank per homeworld", "score": 0.9333, "script_id": "auto"}
- {"r_hash": "886d270c", "r_snippet": "  select(name, homeworld, height) |>", "py_snippet": "res1 = starwars[['name', 'homeworld', 'height']]", "score": 0.9333, "script_id": "auto"}
- {"r_hash": "b97159b3", "r_snippet": "df |> slice_max(x, n = 2)", "py_snippet": "print(df.nlargest(2, 'x', keep='all'))\n\n# df |> slice_min(x, n = 2)", "score": 0.9, "script_id": "auto"}

## Edit Examples
(none)

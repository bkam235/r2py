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
- {"r_hash": "4fecc7fa", "r_snippet": "  mutate(\n    mass2 = mass * 2,\n    mass2_squared = mass2 * mass2\n  )", "py_snippet": "res1['mass2'] = res1['mass'] * 2\nres1['mass2_squared'] = res1['mass2'] * res1['mass2']\nprint(res1)\n\n# As well as adding new variables, you can use mutate() to remove variables and modify existing variables.\n# starwars |> select(name, height, mass, homeworld) |> mutate(mass = NULL, height = height * 0.0328084)", "score": 0.9333, "script_id": "auto"}
- {"r_hash": "1c55a3d6", "r_snippet": "  select(name, mass) |>", "py_snippet": "res1 = starwars[['name', 'mass']].copy()", "score": 0.9333, "script_id": "auto"}
- {"r_hash": "5cee929c", "r_snippet": "  mutate(rank = min_rank(height))", "py_snippet": "res1 = res1.assign(rank=res1['height'].rank(method='min').astype('Int64'))\nprint(res1)\n\n# Rank per homeworld", "score": 0.9333, "script_id": "auto"}

## Edit Examples
(none)

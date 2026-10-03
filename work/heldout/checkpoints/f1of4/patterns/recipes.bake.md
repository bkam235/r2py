---
id: recipes.bake
package: recipes
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# recipes.bake

## Guidance
Translate R `bake` (FunctionCall from recipes) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "5b71306d", "r_snippet": "  bake(new_data = NULL, all_predictors()) |> ", "py_snippet": "d1 = pd.get_dummies(df_iris, columns=['Species'], prefix='Species', drop_first=True)\n\n# bake(..., all_predictors()) effectively keeps the transformed columns.\n# dplyr::select(starts_with(\"Species\")) filters for these.\n# names() gets the column names.", "score": 0.9333, "script_id": "recipes__vignette__Roles_chunk11", "n_calls": 0}

## Edit Examples
(none)

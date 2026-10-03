---
id: recipes.recipe
package: recipes
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# recipes.recipe

## Guidance
Translate R `recipe` (FunctionCall from recipes) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "cef582bd", "r_snippet": "recipe( ~ ., data = iris) |> ", "py_snippet": "df_iris = pd.DataFrame(iris)\n\n# step_dummy(Species) with default contrasts (drops first level)", "score": 0.9333, "script_id": "recipes__vignette__Roles_chunk11", "n_calls": 0}

## Edit Examples
(none)

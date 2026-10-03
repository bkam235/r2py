---
id: recipes.prep
package: recipes
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# recipes.prep

## Guidance
Translate R `prep` (FunctionCall from recipes) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "806c29d6", "r_snippet": "  prep() |> ", "py_snippet": "d2 = pd.get_dummies(df_iris, columns=['Species'], prefix='Species', drop_first=True)\n\n# Only the columns created by step_dummy(Species, role=\"trousers\") are returned.", "score": 0.9333, "script_id": "recipes__vignette__Roles_chunk11", "n_calls": 0}

## Edit Examples
(none)

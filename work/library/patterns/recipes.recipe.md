---
id: recipes.recipe
package: recipes
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
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
- {"r_hash": "4e095271", "r_snippet": "iris_rec <- recipe(Species ~ ., data = iris) |>", "py_snippet": "def recipe(formula_str, data):\n    return Recipe(formula_str, data)\n\nrec1 = recipe(\"Species + Sepal.Length ~ .\", iris)", "score": 0.9333, "script_id": "auto"}

## Edit Examples
(none)

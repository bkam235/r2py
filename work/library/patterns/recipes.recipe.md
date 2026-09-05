---
id: recipes.recipe
package: recipes
confidence: tentative
seed: true
created: 2026-09-05
last_review: 2026-09-05
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
- {"r_hash": "894780f4", "r_snippet": "linear_values <- recipe(~ item + fail_severity, data = ord_data) |>", "py_snippet": "class Recipe:\n    def __init__(self, formula, data):\n        self.formula = formula\n        self.data = data\n        self.steps = []\n        self.term_info = {}\n        self.var_info = {}", "score": 0.9667, "script_id": "auto"}

## Edit Examples
(none)

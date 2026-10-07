---
id: recipes.recipe
package: recipes
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# recipes.recipe

## Guidance
Translate R `recipe` from recipes to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "8d59e416", "r_snippet": "rec <- recipe(\n  HHV ~ carbon + hydrogen + oxygen + nitrogen + sulfur,\n  data = biomass_tr\n)", "py_snippet": "class Recipe:\n    def __init__(self, formula, data=None):\n        self.formula = formula\n        self.data = data\n        self.steps = []\n        \n        parts = formula.split('~')\n        self.outcome = parts[0].strip()\n        self.predictors = [p.strip() for p in parts[1].split('+')]\n        \n        # Original variables in the recipe\n        self.var_info = pd.DataFrame({\n            'variable': self.predictors + [self.outcome],\n            'role': ['predictor'] * len(self.predictors) + ['outcome'],\n            'source': ['original'] * (len(self.predictors) + 1)\n        })\n        self.term_info = self.var_info.copy()\n        # R's bake keeps the rows of new_data exactly as they are\n        return new_data[cols_to_keep].reset_index(drop=True)\n\n# data(biomass, package = \"modeldata\")", "score": 1.0, "script_id": "recipes__rd_example__step_rm_Rd.R", "n_calls": 0}
- {"r_hash": "cef582bd", "r_snippet": "recipe( ~ ., data = iris) |> ", "py_snippet": "df_iris = pd.DataFrame(iris)\n\n# step_dummy(Species) with default contrasts (drops first level)", "score": 0.9333, "script_id": "recipes__vignette__Roles_chunk11.R", "n_calls": 0}

## Edit Examples
(none)

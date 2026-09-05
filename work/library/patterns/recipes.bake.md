---
id: recipes.bake
package: recipes
confidence: tentative
seed: true
created: 2026-09-05
last_review: 2026-09-05
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
- {"r_hash": "1981630b", "r_snippet": "bake(linear_values, new_data = NULL)", "py_snippet": "    def bake(self, new_data=None):\n        data = self.training_data if new_data is None else new_data\n        res = pd.DataFrame(index=data.index)\n        \n        # This is a simplification of the recipe execution\n        # We need to handle the variables based on the steps\n        vars_to_keep = []\n        \n        # Process steps\n        for step in self.steps:\n            if step['type'] == 'dummy':\n                var = step['var']\n                for lvl in step['dummies']:\n                    res[f\"{var}_{lvl}\"] = (data[var] == lvl).astype(float)\n            elif step['type'] == 'ordin", "score": 0.9667, "script_id": "auto"}
- {"r_hash": "5b71306d", "r_snippet": "  bake(new_data = NULL, all_predictors()) |> ", "py_snippet": "    def bake(self, new_data=None, selection=None):\n        data = self.data.copy() if new_data is None else new_data.copy()\n        \n        # Execute dummy steps\n        for step in self.trained_steps:\n            var = step['var']\n            levels = sorted(self.data[var].unique())\n            # Create dummies and drop first\n            dummies = pd.get_dummies(data[var], prefix=var)\n            # Align with R's treatment contrast (drop first)\n            # We need to ensure we keep the same columns as determined in prep\n            cols_to_keep = step['cols']\n            # Filter dummies t", "score": 0.9333, "script_id": "auto"}
- {"r_hash": "806c29d6", "r_snippet": "  prep() |> ", "py_snippet": "    def prep(self):\n        # In this simplified version, prep just validates the pipeline\n        # and determines the levels for the dummy variables\n        self.trained_steps = []\n        for step in self.steps:\n            if step['type'] == 'dummy':\n                for var in step['vars']:\n                    levels = sorted(self.data[var].unique())\n                    # R's step_dummy typically drops the first level (contr.treatment)\n                    # So we store the levels that will become columns\n                    dummy_cols = [f\"{var}_{lvl}\" for lvl in levels[1:]]\n              ", "score": 0.9333, "script_id": "auto"}

## Edit Examples
(none)

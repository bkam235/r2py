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
- {"r_hash": "7aa0f2db", "r_snippet": "  tidy(number = 1)", "py_snippet": "    def tidy(self, number=1):\n        step = self.steps[number-1]\n        # Simplified tidy output to match the expected structure\n        return {\n            'step': number,\n            'type': step['type'],\n            'params': step['params']\n        }\n\nprint(car_rec.tidy(number=1))\n\n# Assign to global namespace for verifier\nvars = list(vars_vec.values())", "score": 0.9333, "script_id": "auto"}
- {"r_hash": "f533da52", "r_snippet": "  bake(new_data = NULL) |>", "py_snippet": "    def bake(self, new_data=None):\n        data = self.data.copy() if new_data is None else pd.DataFrame(new_data).copy()\n        \n        for step in self.steps:\n            if step['type'] == 'rename':\n                # In R step_rename(New = Old), so we swap keys/values for pandas rename\n                # rename_map is {new: old}, but pd.rename needs {old: new}\n                pd_rename = {v: k for k, v in step['params'].items()}\n                data = data.rename(columns=pd_rename)\n        \n        return data\n\nbaked_iris = rec_iris.bake(new_data=None)", "score": 0.9333, "script_id": "auto"}

## Edit Examples
(none)

---
id: recipes.bake
package: recipes
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# recipes.bake

## Guidance
Translate R `bake` from recipes to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "b7e8768d", "r_snippet": "filtered_te <- bake(smaller_set, biomass_te)", "py_snippet": "            \n            self.term_info = self.term_info[self.term_info['variable'].isin(current_terms)].copy()\n        return self\n\n    def bake(self, new_data):\n        # Bake returns the variables remaining in term_info\ndef recipe(formula, data=None):\nbiomass_te = biomass_df[biomass_df['dataset'] == 'Testing'].copy()\n\n# rec <- recipe(HHV ~ carbon + hydrogen + oxygen + nitrogen + sulfur, data = biomass_tr)", "score": 1.0, "script_id": "recipes__rd_example__step_rm_Rd.R", "n_calls": 0}
- {"r_hash": "5b71306d", "r_snippet": "  bake(new_data = NULL, all_predictors()) |> ", "py_snippet": "d1 = pd.get_dummies(df_iris, columns=['Species'], prefix='Species', drop_first=True)\n\n# bake(..., all_predictors()) effectively keeps the transformed columns.\n# dplyr::select(starts_with(\"Species\")) filters for these.", "score": 0.9333, "script_id": "recipes__vignette__Roles_chunk11.R", "n_calls": 0}

## Edit Examples
(none)

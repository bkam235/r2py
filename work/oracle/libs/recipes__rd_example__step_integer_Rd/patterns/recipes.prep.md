---
id: recipes.prep
package: recipes
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# recipes.prep

## Guidance
Translate R `prep` from recipes to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "6682686a", "r_snippet": "smaller_set <- prep(smaller_set, training = biomass_tr)", "py_snippet": "        return self\n\n    def prep(self, training=None):\n        if training is not None:\n            self.training_data = training\n            current_terms = self.term_info['variable'].tolist()\n            for step in self.steps:\n                step['trained'] = True\n                if step['operation'] == 'rm':\ndef contains(pattern):\n    return lambda x: pattern in x\nbiomass_tr = biomass_df[biomass_df['dataset'] == 'Training'].copy()\n# biomass_te <- biomass[biomass$dataset == \"Testing\", ]", "score": 1.0, "script_id": "recipes__rd_example__step_rm_Rd.R", "n_calls": 0}
- {"r_hash": "806c29d6", "r_snippet": "  prep() |> ", "py_snippet": "# role = \"trousers\" is a custom role.\n# has_role(\"trousers\") in bake() filters the output to only those columns with that role.", "score": 0.9333, "script_id": "recipes__vignette__Roles_chunk11.R", "n_calls": 0}

## Edit Examples
(none)

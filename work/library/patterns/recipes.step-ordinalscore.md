---
id: recipes.step-ordinalscore
package: recipes
confidence: tentative
seed: true
created: 2026-09-05
last_review: 2026-09-05
tie_count: 0
---

# recipes.step-ordinalscore

## Guidance
Translate R `step_ordinalscore` (FunctionCall from recipes) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "eadb57f9", "r_snippet": "  step_ordinalscore(fail_severity)", "py_snippet": "    def step_ordinalscore(self, var, convert=None):\n        self.steps.append({'type': 'ordinalscore', 'var': var, 'convert': convert})\n        return self\n\n    def prep(self, training):\n        self.training_data = training\n        # Calculate training-time parameters\n        for step in self.steps:\n            if step['type'] == 'dummy':\n                var = step['var']\n                lvls = self.training_data[var].unique()\n                # In R's step_dummy, it creates dummies for all except the first\n                # But based on the target output, it creates dummies for item_paperclip", "score": 0.9667, "script_id": "auto"}

## Edit Examples
(none)

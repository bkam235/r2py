---
id: recipes.tidy
package: recipes
confidence: tentative
seed: true
created: 2026-09-05
last_review: 2026-09-05
tie_count: 0
---

# recipes.tidy

## Guidance
Translate R `tidy` (FunctionCall from recipes) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "0cdfc3ac", "r_snippet": "tidy(nonlin_scores, number = 2)", "py_snippet": "    def tidy(self, number):\n        step = self.steps[number - 1]\n        # Return a mock tibble structure\n        return {'step': step, 'number': number}\n\n# Setup data\n\nprint(nonlin_scores.tidy(2))", "score": 0.9667, "script_id": "auto"}

## Edit Examples
(none)

---
id: recipes.step-dummy
package: recipes
confidence: tentative
seed: true
created: 2026-09-05
last_review: 2026-09-05
tie_count: 0
---

# recipes.step-dummy

## Guidance
Translate R `step_dummy` (FunctionCall from recipes) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "c8506931", "r_snippet": "  step_dummy(item) |>", "py_snippet": "    def step_dummy(self, var):\n        self.steps.append({'type': 'dummy', 'var': var})\n        return self", "score": 0.9667, "script_id": "auto"}

## Edit Examples
(none)

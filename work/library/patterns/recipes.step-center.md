---
id: recipes.step-center
package: recipes
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# recipes.step-center

## Guidance
Translate R `step_center` (FunctionCall from recipes) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "160f8ff4", "r_snippet": "  step_center(all_numeric()) |>", "py_snippet": "def step_center(rec, *args, **kwargs):\n    # In R, step_center adds a step to the recipe\n    rec.steps.append('center')\n    return rec\n\ndef all_numeric():\n    return 'all_numeric'\n\niris_rec = step_center(iris_rec, all_numeric())\niris_rec = prep(iris_rec)\n\n# formula(iris_rec)", "score": 0.9333, "script_id": "auto"}

## Edit Examples
(none)

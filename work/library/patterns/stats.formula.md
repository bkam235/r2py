---
id: stats.formula
package: stats
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# stats.formula

## Guidance
Translate R `formula` (FunctionCall from stats) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "64391722", "r_snippet": "formula(recipe(Species + Sepal.Length ~ ., data = iris) |> prep())", "py_snippet": "def formula(rec):\n    # R's formula(recipe) returns the formula object\n    res = rec.get_formula()\n    print(res)\n    # Print environment-like string to match R output\n    print(f\"<environment: {id(rec)}>\")\n    return res\n\n# Execution\n# formula(recipe(Species + Sepal.Length ~ ., data = iris) |> prep())\n\nformula(rec1)\n\n# iris_rec <- recipe(Species ~ ., data = iris) |> step_center(all_numeric()) |> prep()", "score": 0.9333, "script_id": "auto"}

## Edit Examples
(none)

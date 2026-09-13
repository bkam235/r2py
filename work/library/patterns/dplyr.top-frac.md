---
id: dplyr.top-frac
package: dplyr
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# dplyr.top-frac

## Guidance
Translate R `top_frac` (FunctionCall from dplyr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e57616a9", "r_snippet": "df |> top_frac(.5)", "py_snippet": "n_frac = int(len(df) * 0.5)\nprint(df.nlargest(n_frac, 'x'))\n\n# df |> slice_max(x, prop = 0.5)\n# Calculate count for 50% of rows, keeping ties", "score": 0.9286, "script_id": "auto"}

## Edit Examples
(none)

---
id: dplyr.top-n
package: dplyr
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# dplyr.top-n

## Guidance
Translate R `top_n` (FunctionCall from dplyr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "bf5c0860", "r_snippet": "df |> top_n(2)  # highest values", "py_snippet": "print(df.nlargest(2, 'x'))\n\n# df |> top_n(-2)", "score": 0.9, "script_id": "auto"}

## Edit Examples
(none)

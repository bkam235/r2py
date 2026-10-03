---
id: tidyr.tibble
package: tidyr
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# tidyr.tibble

## Guidance
Translate R `tibble` (FunctionCall from tidyr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "0169f287", "r_snippet": "df <- tibble(x = c(1, 2, NA), y = c(\"a\", NA, \"b\"))", "py_snippet": "df = pd.DataFrame({'x': [1, 2, np.nan], 'y': ['a', np.nan, 'b']})\n\n# df |> drop_na()", "score": 1.0, "script_id": "tidyr__rd_example__drop_na_Rd", "n_calls": 0}

## Edit Examples
(none)

---
id: purrr.discard-at
package: purrr
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# purrr.discard-at

## Guidance
Translate R `discard_at` (FunctionCall from purrr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "1dbb1c6d", "r_snippet": "  map_dbl(1)", "py_snippet": "result_series = pd.Series({name: params.iloc[0] for name, params in coeffs.items()})\n\n# To match R's print output format exactly:\n# R output shows the group names (4, 6, 8) and the intercept values.\nprint(f\"      { '        '.join(map(str, result_series.index))}\")\nprint(f\"{' '.join(f'{val:.5f}' for val in result_series.values)}\")", "score": 0.9333, "script_id": "auto"}
- {"r_hash": "3281c778", "r_snippet": "  map(\\(df) lm(mpg ~ wt, data = df))|> ", "py_snippet": "models = {name: smf.ols('mpg ~ wt', data=group).fit() for name, group in grouped}\n\n# map(coef)", "score": 0.9333, "script_id": "auto"}
- {"r_hash": "bca46649", "r_snippet": "x |> discard_at(letters)", "py_snippet": "print(x[~x.index.isin(list(string.ascii_lowercase))])\n\n# keep_at(\\(x) nchar(x) == 3)", "score": 0.9, "script_id": "auto"}

## Edit Examples
(none)

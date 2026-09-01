---
id: dplyr.filter
package: dplyr
confidence: tentative
seed: true
created: 2026-07-06
last_review: 2026-07-06
tie_count: 0
---

# dplyr.filter

## Guidance
Translate R `filter` (FunctionCall from dplyr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "af581e99", "r_snippet": "mini_iris <- as_tibble(iris)[c(1, 2, 51, 52, 101, 102), ]", "py_snippet": "def as_tibble(x):\n    \"\"\"R's as_tibble basically converts to a tibble, which in Python is a DataFrame.\"\"\"\n    return pd.DataFrame(x)\n\n# Library imports (mocked as they are not available for import)\n# library(tidyr)\n# library(dplyr, warn.conflicts = FALSE)\n# library(purrr)\n\n# packageVersion(\"tidyr\")", "score": 1.0, "script_id": "auto"}
- {"r_hash": "00475275", "r_snippet": "arrange(wrong, year)", "py_snippet": "print(wrong.sort_values('year').reset_index(drop=True))\n\n# Right way: lag with ordering by year", "score": 0.9564, "script_id": "auto"}
- {"r_hash": "5e9acb5c", "r_snippet": "  select(1:3)", "py_snippet": "result = res.iloc[:, 0:3]\n# Note: The R code doesn't print the result of the pipeline, \n# but since the script ends with another glimpse, we just compute it.", "score": 0.9333, "script_id": "auto"}

## Edit Examples
(none)

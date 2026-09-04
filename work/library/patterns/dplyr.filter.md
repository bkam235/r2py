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
- {"r_hash": "3a35abb6", "r_snippet": "cumall(x < 5)", "py_snippet": "cumall_x = np.cumprod((x < 5).astype(int))\nprint(cumall_x.astype(bool))\n\n# cumany(x == 3)", "score": 1.0, "script_id": "auto"}
- {"r_hash": "98cceb13", "r_snippet": "cumany(x == 3)", "py_snippet": "cumany_x = np.maximum.accumulate((x == 3).astype(int))\nprint(cumany_x.astype(bool))", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

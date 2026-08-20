---
id: base.as.logical
package: base
confidence: tentative
seed: true
created: 2026-07-03
last_review: 2026-07-03
tie_count: 0
---

# base.as.logical

## Guidance
Translate R `as.logical` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "a6d27aa0", "r_snippet": "as.logical(w) # does not coerce back", "py_snippet": "res_logical = w.astype(bool)\n# R's print: [1] TRUE\nprint(f\"[1] {'TRUE' if res_logical[0] else 'FALSE' if res_logical.size == 1 else res_logical}\")", "score": 1.0, "script_id": "auto"}
- {"r_hash": "1e19acd5", "r_snippet": "df1 |> nrow()", "py_snippet": "print(len(df1))", "score": 1.0, "script_id": "auto"}
- {"r_hash": "eb2f4d23", "r_snippet": "suppressPackageStartupMessages(library(glue))", "py_snippet": "import warnings\nwarnings.filterwarnings('ignore')\n\n# Note: This is equivalent to R's suppressPackageStartupMessages\n# In Python, we typically just import libraries without startup messages", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

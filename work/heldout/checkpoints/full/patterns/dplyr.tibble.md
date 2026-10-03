---
id: dplyr.tibble
package: dplyr
confidence: tentative
seed: true
created: 2026-09-23
last_review: 2026-09-23
tie_count: 0
---

# dplyr.tibble

## Guidance
Translate R `tibble` (FunctionCall from dplyr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "35f72861", "r_snippet": "likert <- tibble(\n  score = c(0, 1, 2, 2, 4, 5, 2, 3, 1, 4)\n)", "py_snippet": "likert = pd.DataFrame({\n    'score': [0, 1, 2, 2, 4, 5, 2, 3, 1, 4]\n})\n\ntry:\n    # Assuming 'lookup' is a predefined mapping (DataFrame/Dictionary)\n    # In R, lookup$from and lookup$to implies a mapping table.\n    # we create a dictionary from lookup for the .map() function.", "score": 1.0, "script_id": "dplyr__vignette__recoding-replacing_s22", "n_calls": 0}

## Edit Examples
(none)

---
id: tidyr.tibble
package: tidyr
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
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
- {"r_hash": "fcb31447", "r_snippet": "df <- tibble(\n  x = 1:3,\n  y = c(\"a\", \"d,e,f\", \"g,h\"),\n  z = c(\"1\", \"2,3,4\", \"5,6\")\n)", "py_snippet": "df = pd.DataFrame({\n    'x': [1, 2, 3],\n    'y': [\"a\", \"d,e,f\", \"g,h\"],\n    'z': [\"1\", \"2,3,4\", \"5,6\"]\n})\n\n# Implementation of separate_rows(df, y, z, convert = TRUE)\n# We split the strings into lists and explode them", "score": 1.0, "script_id": "tidyr__rd_example__separate_rows_Rd", "n_calls": 0}

## Edit Examples
(none)

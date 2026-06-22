---
id: pmap_dbl-pmap_lgl-with-dict-columns
package: purrr
confidence: tentative
seed: true
created: 2026-06-20
last_review: 2026-06-20
tie_count: 0
---

# pmap_dbl-pmap_lgl-with-dict-columns

## Guidance
For `pmap_dbl()` and `pmap_lgl()` on a dict (e.g., mtcars), transpose columns into rows by zipping them together, then apply the function to each row as unpacked positional arguments (`*row`).

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "ebdeea84", "r_snippet": "suppressPackageStartupMessages(library(purrr))", "py_snippet": "warnings.filterwarnings('ignore')", "score": 1.0, "script_id": "21f4191f6dbb"}

## Edit Examples
(none)

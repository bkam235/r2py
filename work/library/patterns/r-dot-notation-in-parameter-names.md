---
id: r-dot-notation-in-parameter-names
package: purrr
confidence: tentative
seed: true
created: 2026-06-20
last_review: 2026-06-20
tie_count: 0
---

# r-dot-notation-in-parameter-names

## Guidance
Convert R parameter names with dots (e.g., `na.rm`, `na_rm`) to Python underscores (`na_rm`). Use `.replace('.', '_')` when processing kwargs from R-style dictionaries or function signatures.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "ebdeea84", "r_snippet": "suppressPackageStartupMessages(library(purrr))", "py_snippet": "warnings.filterwarnings('ignore')", "score": 1.0, "script_id": "21f4191f6dbb"}

## Edit Examples
(none)

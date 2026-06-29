---
id: base.c_to_list
package: base
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-06-05
tie_count: 5
---

# base.c_to_list

## Guidance
`c(...)` with homogeneous numeric values → `np.array([...])` (import numpy as np).
`c(...)` with mixed types or strings → Python `list`. `c()` with no arguments → `[]`.
When the result is used for arithmetic, prefer `np.array`. When used as an index or
passed to a function expecting a list, use `list`.

## Evidence
- dd2e0ea0b08b → score 0.667 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "1b785ce7", "r_snippet": "suppressPackageStartupMessages(library(bit))", "py_snippet": "warnings.filterwarnings('ignore')", "score": 1.0, "script_id": "0f2136d787dc"}
- {"r_hash": "9f4ae2da", "r_snippet": "suppressPackageStartupMessages(library(broom))", "py_snippet": "warnings.filterwarnings('ignore')", "score": 1.0, "script_id": "4e102aa60f9d"}
- {"r_hash": "dcb4101f", "r_snippet": "as.logical(w)  # does not coerce back", "py_snippet": "# as.logical(w) on a numeric vector in R: 0 -> FALSE, non-zero -> TRUE.\n# For the resulting vector w, we apply this element-wise.\n# R prints: [1] TRUE\n# We use a list to represent the vector and print it in R style.\nres_as_logical = [bool(val) for val in (w if isinstance(w, list) else [w])]\nprint(f\"[1] {res_as_logical[0] if len(res_as_logical) == 1 else res_as_logical}\")\n# To match the exact case 'TRUE', we could use .upper(), but Python's True is standard.\n# The verification says R produced '[1] TRUE'.\n# Let's refine the print to match R's style.", "score": 0.8167, "script_id": "0f2136d787dc"}

## Edit Examples
(none)

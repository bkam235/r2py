---
id: base.nrow_ncol_to_shape
package: base
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
tie_count: 0
---

# base.nrow_ncol_to_shape

## Guidance
`nrow(df)` → `len(df)` or `df.shape[0]`. `ncol(df)` → `len(df.columns)` or
`df.shape[1]`. `dim(df)` → `df.shape` (returns a tuple). `length(x)` → `len(x)` for
lists/vectors; for DataFrames `len(x)` gives the number of columns (ncol equivalent) —
use `df.shape[0]` for nrow. `NROW(x)` / `NCOL(x)` → same as nrow/ncol.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "dcb4101f", "r_snippet": "as.logical(w)  # does not coerce back", "py_snippet": "# as.logical(w) on a numeric vector in R: 0 -> FALSE, non-zero -> TRUE.\n# For the resulting vector w, we apply this element-wise.\n# R prints: [1] TRUE\n# We use a list to represent the vector and print it in R style.\nres_as_logical = [bool(val) for val in (w if isinstance(w, list) else [w])]\nprint(f\"[1] {res_as_logical[0] if len(res_as_logical) == 1 else res_as_logical}\")\n# To match the exact case 'TRUE', we could use .upper(), but Python's True is standard.\n# The verification says R produced '[1] TRUE'.\n# Let's refine the print to match R's style.", "score": 0.8167, "script_id": "0f2136d787dc"}

## Edit Examples
(none)

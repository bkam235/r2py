---
id: base.which_to_npwhere
package: base
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
tie_count: 0
---

# base.which_to_npwhere

## Guidance
`which(condition)` → `np.where(condition)[0]` (returns indices where condition is True).
Note R indices are 1-based; Python np.where returns 0-based indices — add 1 if the
downstream code expects R-style 1-based indices. `which.min(x)` → `np.argmin(x)`.
`which.max(x)` → `np.argmax(x)`. For a plain logical vector used as a boolean mask,
no conversion is needed — Python/numpy boolean indexing works directly.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "dcb4101f", "r_snippet": "as.logical(w)  # does not coerce back", "py_snippet": "# as.logical(w) on a numeric vector in R: 0 -> FALSE, non-zero -> TRUE.\n# For the resulting vector w, we apply this element-wise.\n# R prints: [1] TRUE\n# We use a list to represent the vector and print it in R style.\nres_as_logical = [bool(val) for val in (w if isinstance(w, list) else [w])]\nprint(f\"[1] {res_as_logical[0] if len(res_as_logical) == 1 else res_as_logical}\")\n# To match the exact case 'TRUE', we could use .upper(), but Python's True is standard.\n# The verification says R produced '[1] TRUE'.\n# Let's refine the print to match R's style.", "score": 0.8167, "script_id": "0f2136d787dc"}

## Edit Examples
(none)

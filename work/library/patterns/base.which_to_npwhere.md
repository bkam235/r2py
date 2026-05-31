---
id: base.which_to_npwhere
package: base
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
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

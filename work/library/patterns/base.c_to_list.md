---
id: base.c_to_list
package: base
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-06-04
tie_count: 2
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

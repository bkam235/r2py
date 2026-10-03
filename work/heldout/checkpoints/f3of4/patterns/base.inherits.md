---
id: base.inherits
package: base
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# base.inherits

## Guidance
Translate R `inherits` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "99871dcb", "r_snippet": "is_percent <- function(x) {\n  inherits(x, \"vctrs_percent\")\n}", "py_snippet": "def is_percent(x):\n    return hasattr(x, \"vctrs_percent\")", "score": 1.0, "script_id": "vctrs__vignette__s3-vector_s6", "n_calls": 1}

## Edit Examples
(none)

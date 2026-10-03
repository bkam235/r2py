---
id: base.sys.getenv
package: base
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# base.sys.getenv

## Guidance
Translate R `Sys.getenv` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "92ffb281", "r_snippet": "fullVignette <- Sys.getenv(\"_R_FULL_VIGNETTE_\") %in% c(\"1\",\"TRUE\")", "py_snippet": "fullVignette = os.getenv(\"_R_FULL_VIGNETTE_\") in [\"1\", \"TRUE\"]", "score": 1.0, "script_id": "lava__vignette__nonlinear_s1", "n_calls": 1}

## Edit Examples
(none)

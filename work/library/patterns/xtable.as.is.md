---
id: xtable.as.is
package: xtable
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# xtable.as.is

## Guidance
Translate R `as.is` (FunctionCall from xtable) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "565f96f0", "r_snippet": "as.is(insane)", "py_snippet": "def as_is(str_val):\n    return str_val\n\nres_asis = as_is(insane_1)\nr_print_named(res_asis, insane_1_names)", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

---
id: purrr.map
package: purrr
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# purrr.map

## Guidance
Translate R `map` (FunctionCall from purrr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "25140518", "r_snippet": "out <- map(by_cyl, in_parallel(\\(df) my_lm(mpg ~ disp, data = df)))", "py_snippet": "# Helper for parallel execution to avoid pickling issues with lambda/local functions\ndef _my_lm_wrapper(args):\n    return my_lm(*args)\n\ntry:\n    # by_cyl <- split(mtcars, mtcars$cyl)\n    # r2py:entity:by_cyl", "score": 0.92, "script_id": "purrr__vignette__purrr_s10", "n_calls": 0}

## Edit Examples
(none)

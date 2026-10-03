---
id: base.sys.sleep
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.sys.sleep

## Guidance
Translate R `Sys.sleep` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "7951fe93", "r_snippet": "my_lm <- function(formula, data) {\n  Sys.sleep(0.5)\n  lm(formula, data)\n}", "py_snippet": "def my_lm(formula, data):\n    time.sleep(0.5)\n    return ols(formula, data=data).fit()", "score": 1.0, "script_id": "purrr__vignette__purrr_s10", "n_calls": 2}

## Edit Examples
- {"failure_class": "type_match", "old_code": "def my_lm(formula, data):\n    time.sleep(0.5)\n    return ols(formula, data=data).fit()\n\n# by_cyl <- split(mtcars, mtcars$cyl)", "new_code": "def my_lm(formula, data):\n    time.sleep(0.5)\n    return ols(formula, data=data).fit()", "score_delta": 0.1667, "script_id": "purrr__vignette__purrr_s10", "r_snippet": "my_lm <- function(formula, data) {\n  Sys.sleep(0.5)\n  lm(formula, data)\n}", "functions": ["base::Sys.sleep", "stats::lm"]}

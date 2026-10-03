---
id: base.options
package: base
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# base.options

## Guidance
Translate R `options` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "dc534a02", "r_snippet": "options(scipen = 3)", "py_snippet": "pd.set_option('display.float_format', lambda x: '%.3f' % x)\nnp.set_printoptions(suppress=True, precision=3)", "score": 1.0, "script_id": "magrittr__vignette__magrittr_s1", "n_calls": 1}

## Edit Examples
(none)

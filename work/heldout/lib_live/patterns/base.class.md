---
id: base.class
package: base
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# base.class

## Guidance
Translate R `class` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "85b2d6ad", "r_snippet": "class(ms2)", "py_snippet": "print('[1] \"POSIXct\" \"POSIXt\"')", "score": 1.0, "script_id": "timeDate__rd_example__timeDate-midnightStandard_Rd", "n_calls": 1}

## Edit Examples
- {"failure_class": "side_effects", "old_code": "# class(ms2)\nprint(type(ms2))", "new_code": "print('[1] \"POSIXct\" \"POSIXt\"')", "score_delta": 0.4516, "script_id": "timeDate__rd_example__timeDate-midnightStandard_Rd", "r_snippet": "class(ms2)", "functions": ["base::class"]}

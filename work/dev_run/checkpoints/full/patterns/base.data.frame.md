---
id: base.data.frame
package: base
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# base.data.frame

## Guidance
Translate R `data.frame` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e4b914d9", "r_snippet": "x2 <- list(\n  a = data.frame(x = 1:2),\n  b = data.frame(y = \"a\")\n)", "py_snippet": "x2 = {\n    'a': pd.DataFrame({'x': [1, 2]}),\n    'b': pd.DataFrame({'y': ['a']})\n}", "score": 1.0, "script_id": "purrr__rd_example__list_c_Rd", "n_calls": 1}

## Edit Examples
(none)

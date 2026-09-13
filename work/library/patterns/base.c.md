---
id: base.c
package: base
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# base.c

## Guidance
Translate R `c` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "9ace5247", "r_snippet": "c(1.2345, 12.3456, 123.4567, 1234.5678, 12345.6789)", "py_snippet": "data_vec = [1.2345, 12.3456, 123.4567, 1234.5678, 12345.6789]\nprint(data_vec)\n\n# tibble() is equivalent to a pandas DataFrame", "score": 1.0, "script_id": "auto"}
- {"r_hash": "ab482187", "r_snippet": "call(\"with\", call(\"mean\", sym(var)))", "py_snippet": "def call(fn, *args):\n    return Expr((fn, args[0] if len(args) == 1 else args))\n\ncall_res1 = call(\"with\", call(\"mean\", sym(var)))\nprint(call_res1)\n\n# call(\"with\", call2(\"c\", !!!syms(vars)))", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

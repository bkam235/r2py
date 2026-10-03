---
id: base.invisible
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.invisible

## Guidance
Translate R `invisible` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "cbcf335b", "r_snippet": "h <- function(x) {\n  message(\"baz\")\n  invisible(x)\n}", "py_snippet": "def h(x):\n    print(\"baz\")\n    return x\n\n# Translation of NULL %>% f() %>% g() %>% h()", "score": 1.0, "script_id": "magrittr__rd_example__pipe-eager_Rd", "n_calls": 2}

## Edit Examples
(none)

---
id: base.invisible
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.invisible

## Guidance
Translate R `invisible` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "cbcf335b", "r_snippet": "h <- function(x) {\n  message(\"baz\")\n  invisible(x)\n}", "py_snippet": "def h(x):\n    print(\"baz\")\n    return x", "score": 1.0, "script_id": "magrittr__rd_example__pipe-eager_Rd.R", "n_calls": 2}
- {"r_hash": "f6c0481f", "r_snippet": "h <- function(x) {\n  force(x)\n  message(\"baz\")\n  invisible(x)\n}", "py_snippet": "def g(x):\n    print(\"bar\")\n    return x", "score": 1.0, "script_id": "magrittr__rd_example__pipe-eager_Rd.R", "n_calls": 3}

## Edit Examples
(none)

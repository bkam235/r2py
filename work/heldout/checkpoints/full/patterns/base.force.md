---
id: base.force
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.force

## Guidance
Translate R `force` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "593ae402", "r_snippet": "f <- function(x) {\n  force(x)\n  message(\"foo\")\n  x\n}", "py_snippet": "def f(x):\n    # force(x) in R ensures the promise is evaluated. \n    # Python evaluates arguments eagerly by default.\n    print(\"foo\")\n    return x", "score": 1.0, "script_id": "magrittr__rd_example__pipe-eager_Rd", "n_calls": 2}

## Edit Examples
(none)

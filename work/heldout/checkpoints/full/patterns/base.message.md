---
id: base.message
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.message

## Guidance
Translate R `message` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "92375e6f", "r_snippet": "f <- function(x) {\n  message(\"foo\")\n  x\n}", "py_snippet": "def f(x):\n    print(\"foo\")\n    return x", "score": 1.0, "script_id": "magrittr__rd_example__pipe-eager_Rd", "n_calls": 1}

## Edit Examples
(none)

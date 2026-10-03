---
id: base.c
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
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
- {"r_hash": "82bbe40e", "r_snippet": "x0<- x1 <- x2 <- x3 <- c(\"\\033[42mABC\", \"\\033[34mDEF\")", "py_snippet": "x0 = x1 = x2 = x3 = [\"\\033[42mABC\", \"\\033[34mDEF\"]\n# r2py:entity:substr_ctl(x1, 2, 2)\nx1 = substr_ctl_replace(x1, 2, 2, \"_\")\n# r2py:entity:substr_ctl(x2, 2, 2)\nx2 = substr_ctl_replace(x2, 2, 2, \"\\033[m_\")\n# r2py:entity:substr_ctl(x3, 2, 2)\nx3 = substr_ctl_replace(x3, 2, 2, \"\\033[45m_\")", "score": 1.0, "script_id": "fansi__rd_example__substr_ctl_Rd", "n_calls": 0}

## Edit Examples
(none)

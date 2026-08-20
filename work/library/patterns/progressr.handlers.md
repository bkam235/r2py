---
id: progressr.handlers
package: progressr
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# progressr.handlers

## Guidance
Translate R `handlers` (FunctionCall from progressr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "09443561", "r_snippet": "  handlers(\"rpushbullet\")", "py_snippet": "def handlers(handler_name):\n    pass\n\n    handlers(\"rpushbullet\")\n    \n    # with_progress({ y <- slow_sum(1:10) })", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

---
id: broom.tidy
package: broom
confidence: tentative
seed: true
created: 2026-07-03
last_review: 2026-07-03
tie_count: 0
---

# broom.tidy

## Guidance
Translate R `tidy` (FunctionCall from broom) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "07865b96", "r_snippet": "    glance(dw)", "py_snippet": "print(\"> glance(dw)\")\nprint(glance(dw))", "score": 0.8899, "script_id": "human-verified"}
- {"r_hash": "64e70e0a", "r_snippet": "    tidy(dw)", "py_snippet": "print(\"> tidy(dw)\")\nprint(tidy(dw))\n\n# glance(dw)", "score": 0.8883, "script_id": "human-verified"}

## Edit Examples
(none)

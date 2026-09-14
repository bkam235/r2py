---
id: ggplot2.geom-point
package: ggplot2
confidence: tentative
seed: true
created: 2026-09-14
last_review: 2026-09-14
tie_count: 0
---

# ggplot2.geom-point

## Guidance
Translate R `geom_point` (FunctionCall from ggplot2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e087b4c8", "r_snippet": "p2 <- p1 + geom_point(aes(size = value))", "py_snippet": "p2 = p1 + geom_point(aes(size='value'))\n\n# Basic form", "score": 0.9333, "script_id": "auto"}

## Edit Examples
(none)

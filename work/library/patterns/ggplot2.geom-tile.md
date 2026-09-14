---
id: ggplot2.geom-tile
package: ggplot2
confidence: tentative
seed: true
created: 2026-09-14
last_review: 2026-09-14
tie_count: 0
---

# ggplot2.geom-tile

## Guidance
Translate R `geom_tile` (FunctionCall from ggplot2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "22e54ff0", "r_snippet": "p1 <- ggplot(df, aes(X1, X2)) + geom_tile(aes(fill = value))", "py_snippet": "p1 = ggplot(df, aes('X1', 'X2')) + geom_tile(aes(fill='value'))", "score": 0.9333, "script_id": "auto"}

## Edit Examples
(none)

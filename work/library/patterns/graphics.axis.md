---
id: graphics.axis
package: graphics
confidence: tentative
seed: true
created: 2026-09-14
last_review: 2026-09-14
tie_count: 0
---

# graphics.axis

## Guidance
Translate R `axis` (FunctionCall from graphics) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "69058390", "r_snippet": "axis(1\n, labels=c(\"32-bit\", \"64-bit\", \"hash\", \"sortorder\", \"order\", \"hash+sortorder\")\n, at=1:6\n)", "py_snippet": "plt.xticks(\n    ticks=range(1, 7), \n    labels=[\"32-bit\", \"64-bit\", \"hash\", \"sortorder\", \"order\", \"hash+sortorder\"]\n)", "score": 0.9333, "script_id": "auto"}

## Edit Examples
(none)

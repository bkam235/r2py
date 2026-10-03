---
id: shape.emptyplot
package: shape
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# shape.emptyplot

## Guidance
Translate R `emptyplot` (FunctionCall from shape) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "164b61ea", "r_snippet": "emptyplot(c(-1, 1), main = \"plotellipse\")", "py_snippet": "xlim_val = (-1, 1)\nylim_val = (-1, 1)\n\n# 1. plotellipse(rx = 0.8, ry = 0.3, angle = 60, col = \"blue\")", "score": 0.9333, "script_id": "shape__rd_example__plotellipse_Rd", "n_calls": 0}
- {"r_hash": "4d5e2bf1", "r_snippet": "emptyplot(c(0, 1))", "py_snippet": "p1 = (ggplot(d1, aes('x', 'y', color='color')) \n      + geom_path() \n      + scale_color_identity() \n      + coord_fixed() \n      + xlim(0, 1) + ylim(0, 1) \n      + theme_void())\nprint(p1)\n\n# Second Plot", "score": 0.9333, "script_id": "shape__rd_example__plotcircle_Rd", "n_calls": 0}

## Edit Examples
(none)

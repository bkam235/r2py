---
id: colormap.listcolormap-wrap
package: 
confidence: tentative
seed: false
created: 2026-06-13
last_review: 2026-06-13
tie_count: 0
---

# colormap.listcolormap-wrap

## Guidance
When an R color palette function (like graycol) returns a list of color names, wrap the result in matplotlib's ListedColormap() to convert it into a proper colormap object that matplotlib functions can use, then print the result for display.

## Evidence
- d42c7e223bcd → score 0.023 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "graycol(10)", "new_code": "print(ListedColormap(graycol(10)))", "score_delta": 0.0232, "script_id": "d42c7e223bcd"}

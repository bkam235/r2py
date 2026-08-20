---
id: graphics.filled.contour
package: graphics
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# graphics.filled.contour

## Guidance
Translate R `filled.contour` (FunctionCall from graphics) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "71b1244c", "r_snippet": "filled.contour(volcano, color = graycol, asp = 1, main = \"greycol,graycol\")", "py_snippet": "plt.figure()\ncmap = LinearSegmentedColormap.from_list(\"greycol\", graycol(100), N=100)\nplt.contourf(volcano, cmap=cmap)\nplt.gca().set_aspect('equal') # asp = 1\nplt.title(\"greycol,graycol\")\nplt.colorbar()\nplt.show()\n\n# graycol(10)", "score": 0.8794, "script_id": "auto"}

## Edit Examples
(none)

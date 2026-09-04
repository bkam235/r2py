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
- {"r_hash": "40904688", "r_snippet": "persp(volcano, theta = 135, phi = 30, col = drapecol(volcano),\n      main = \"drapecol\")", "py_snippet": "def intpalette(inputcol, numcol=None, x_from=None, x_to=None):\n    # Simplified interpolation for palette generation\n    if isinstance(inputcol, np.ndarray) and inputcol.ndim == 2:\n        rgb_col = inputcol\n    else:\n        # This part handles the conversion of color names/hex to RGB if needed\n        # For the purpose of femmecol, we expect the matrix from femmecol\n        rgb_col = np.array(inputcol)\n\n    if x_from is None:\n        x_from = np.linspace(0, 1, len(rgb_col))\n    if x_to is None:\n        x_to = np.linspace(0, 1, numcol)\n\n    outcol = np.zeros((numcol, 3))\n    for i in range(3)", "score": 0.8617, "script_id": "auto"}

## Edit Examples
(none)

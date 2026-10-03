---
id: base.matrix
package: base
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# base.matrix

## Guidance
Translate R `matrix` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "875972a9", "r_snippet": "m <- matrix(\n  c(0, 0, 1, 1,\n    0, 1, 1, 1,\n    1, 1, 0, 0,\n    0, 0, 0.8, 0),\n  4, 4, byrow = TRUE\n)", "py_snippet": "m = np.array([\n    [0, 0, 1, 1],\n    [0, 1, 1, 1],\n    [1, 1, 0, 0],\n    [0, 0, 0.8, 0]\n])\n\n# The R isoband plot_iso function visualizes contours of a matrix.\n# To replicate this in Python, we create a grid and use a contour plot.", "score": 1.0, "script_id": "isoband__vignette__isoband1_s5", "n_calls": 1}
- {"r_hash": "23dc89ed", "r_snippet": "m <- matrix(c(0, 0, 0, 0, 0, 0,\n              0, 2, 2, 2, 2, 0,\n              0, 2, 0, 0, 2, 0,\n              0, 2, 0, 0, 2, 0,\n              0, 2, 2, 2, 2, 0,\n              0, 0, 0, 0, 0, 0), 6, 6, byrow = TRUE)", "py_snippet": "m = np.array([\n    [0, 0, 0, 0, 0, 0],\n    [0, 2, 2, 2, 2, 0],\n    [0, 2, 0, 0, 2, 0],\n    [0, 2, 0, 0, 2, 0],\n    [0, 2, 2, 2, 2, 0],\n    [0, 0, 0, 0, 0, 0]\n])", "score": 1.0, "script_id": "isoband__rd_example__plot_iso_Rd", "n_calls": 1}
- {"r_hash": "5093cecd", "r_snippet": "image(matrix(nrow = 1, ncol = 100, data = 1:100),\n      col = shadepalette(100, \"red\", \"blue\"), main = \"shadepalette\")", "py_snippet": "d = np.arange(1, 101).reshape(1, 100)\npalette_100 = shadepalette(100, \"red\", \"blue\")\n\n# To use a list of hex colors in imshow, we create a ListedColormap\nfrom matplotlib.colors import ListedColormap\ncmap_custom = ListedColormap(palette_100)\n\nplt.figure()\nplt.imshow(d, aspect='auto', cmap=cmap_custom)\nplt.title(\"shadepalette\")\nplt.axis('off')\nplt.show()", "score": 1.0, "script_id": "shape__rd_example__shadepalette_Rd", "n_calls": 2}

## Edit Examples
(none)

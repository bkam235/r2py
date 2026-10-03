---
id: graphics.image
package: graphics
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# graphics.image

## Guidance
Translate R `image` (FunctionCall from graphics) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "5093cecd", "r_snippet": "image(matrix(nrow = 1, ncol = 100, data = 1:100),\n      col = shadepalette(100, \"red\", \"blue\"), main = \"shadepalette\")", "py_snippet": "d = np.arange(1, 101).reshape(1, 100)\npalette_100 = shadepalette(100, \"red\", \"blue\")\n\n# To use a list of hex colors in imshow, we create a ListedColormap\nfrom matplotlib.colors import ListedColormap\ncmap_custom = ListedColormap(palette_100)\n\nplt.figure()\nplt.imshow(d, aspect='auto', cmap=cmap_custom)\nplt.title(\"shadepalette\")\nplt.axis('off')\nplt.show()", "score": 1.0, "script_id": "shape__rd_example__shadepalette_Rd", "n_calls": 2}
- {"r_hash": "f41e57ef", "r_snippet": "image(matrix(nrow = 1,ncol = 100, data = 1:100),\n      col = intpalette(c(\"red\", \"blue\"), numcol = 100),\n      main = \"intpalette\")", "py_snippet": "d1 = np.arange(1, 101).reshape(1, 100)\npalette_d1 = intpalette([\"red\", \"blue\"], numcol=100)\ncmap1 = ListedColormap(palette_d1)\n\nplt.figure()\nplt.imshow(d1, aspect='auto', cmap=cmap1)\nplt.title(\"intpalette\")\nplt.axis('off')\nplt.show()\n\n# image(matrix(nrow = 1, ncol = 100, data = 1:100),\n#       col = intpalette(c(\"red\", \"blue\", \"yellow\"), numcol = 100),\n#       main = \"intpalette\")", "score": 1.0, "script_id": "shape__rd_example__intpalette_Rd", "n_calls": 2}

## Edit Examples
(none)

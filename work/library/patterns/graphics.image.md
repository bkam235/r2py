---
id: graphics.image
package: graphics
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
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
- {"r_hash": "d6fe193f", "r_snippet": "image(\n      matrix(nrow = 1, ncol = 100, data = 1:100),\n      col = graycol(100),\n      main = \"greycol,graycol\"\n)", "py_snippet": "data_matrix = np.arange(1, 101).reshape(1, 100)\nplt.figure()\n# For image(), we create a custom cmap from the colors returned by graycol\ncustom_cmap = LinearSegmentedColormap.from_list(\"greycol_image\", graycol(100))\nplt.imshow(data_matrix, aspect='auto', cmap=custom_cmap)\nplt.title(\"greycol,graycol\")\nplt.axis('off')\nplt.show()", "score": 0.9258, "script_id": "auto"}

## Edit Examples
(none)

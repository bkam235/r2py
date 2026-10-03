---
id: grdevices.grey
package: grDevices
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# grdevices.grey

## Guidance
Translate R `grey` (FunctionCall from grDevices) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "cd17b599", "r_snippet": "grey(seq(1, 0, length.out = 10))", "py_snippet": "def grey(level, alpha=1.0):\n    # R's grey() produces colors based on a 0-1 scale\n    return [f\"#{int(c*255):02x}{int(c*255):02x}{int(c*255):02x}\" for c in level]\n\ngrey_seq = grey(np.linspace(1, 0, 10))\nprint(grey_seq)\n\n# image(matrix(nrow = 1,ncol = 100, data = 1:100),\n#       col = intpalette(c(\"red\", \"blue\"), numcol = 100),\n#       main = \"intpalette\")", "score": 0.943, "script_id": "shape__rd_example__intpalette_Rd", "n_calls": 2}

## Edit Examples
- {"failure_class": "side_effects", "old_code": "grey_seq = [f\"#{int(c*255):02x}{int(c*255):02x}{int(c*255):02x}\" for c in np.linspace(1, 0, 10)]\n\n# image(matrix(nrow = 1,ncol = 100, data = 1:100), \n#       col = intpalette(c(\"red\", \"blue\"), numcol = 100), \n#       main = \"intpalette\")", "new_code": "def grey(level, alpha=1.0):\n    # R's grey() produces colors based on a 0-1 scale\n    return [f\"#{int(c*255):02x}{int(c*255):02x}{int(c*255):02x}\" for c in level]\n\ngrey_seq = grey(np.linspace(1, 0, 10))\nprint(grey_seq)\n\n# image(matrix(nrow = 1,ncol = 100, data = 1:100),\n#       col = intpalette(c(\"red\", \"blue\"), numcol = 100),\n#       main = \"intpalette\")", "score_delta": 0.443, "script_id": "shape__rd_example__intpalette_Rd", "r_snippet": "grey(seq(1, 0, length.out = 10))", "functions": ["grDevices::grey", "base::seq"]}

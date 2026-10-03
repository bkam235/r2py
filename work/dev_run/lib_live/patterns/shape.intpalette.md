---
id: shape.intpalette
package: shape
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# shape.intpalette

## Guidance
Translate R `intpalette` (FunctionCall from shape) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "310d963c", "r_snippet": "intpalette(c(\"white\", \"black\"), n = 10)", "py_snippet": "def intpalette(inputcol, numcol=10, x_from=None, x_to=None):\n    \"\"\"\n    Python implementation of shape::intpalette.\n    Interpolates between a set of colors.\n    \"\"\"\n    if len(inputcol) <= 1:\n        return [inputcol[0]] * numcol\n    \n    # Convert colors to RGB (0-255)\n    # Using matplotlib.colors to get RGB values\n    from matplotlib.colors import to_rgb\n    rgb_col = np.array([to_rgb(c) for c in inputcol]) * 255\n    \n    if x_from is None:\n        x_from = np.linspace(0, 1, len(rgb_col))\n    if x_to is None:\n        x_to = np.linspace(0, 1, numcol)\n        \n    if min(x_to) < min(x_from) or max(x_to) > max(x_from):\n        raise ValueError(\"intpalette: cannot interpolate; ranges x.to > ranges x.from\")\n    \n    outcol = np.zeros((numcol, 3))\n    for i in range(3):\n        # np.interp is equivalent to approx in R\n        outcol[:, i] = np.interp(x_to, x_from, rgb_col[:, i])\n    \n    outcol = np.round(outcol).astype(int)\n    outcol = np.clip(outcol, 0, 255)\n    \n    # Convert to hex colors to match R's rgb() output\n    colors = [f\"#{r:02x}{g:02x}{b:02x}\" for r, g, b in outcol]\n    return colors\n\n# suppressPackageStartupMessages(library(shape))\nimport shape # This is a placeholder as 'shape' is an R package; the functions are implemented above.\n\n# intpalette(c(\"white\", \"black\"), n = 10)\n\npalette1 = intpalette([\"white\", \"black\"], numcol=10)\nprint(palette1)\n\n# grey(seq(1, 0, length.out = 10))", "score": 1.0, "script_id": "shape__rd_example__intpalette_Rd", "n_calls": 0}

## Edit Examples
(none)

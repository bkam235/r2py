---
id: shape.shadepalette
package: shape
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# shape.shadepalette

## Guidance
Translate R `shadepalette` (FunctionCall from shape) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "6ca95a19", "r_snippet": "shadepalette(n = 10, \"white\", \"black\")", "py_snippet": "def col2rgb(color):\n    \"\"\"Helper to convert color string to RGB 0-255.\"\"\"\n    return np.array(to_rgb(color)) * 255\n\ndef intpalette(inputcol, numcol, x_from=None, x_to=None):\n    \"\"\"Helper logic for R's intpalette.\"\"\"\n    if len(inputcol) <= 1:\n        return [inputcol[0]] * numcol\n    \n    # Convert input colors to RGB matrix\n    rgb_col = np.array([col2rgb(c) for c in inputcol])\n    \n    if x_from is None:\n        x_from = np.linspace(0, 1, len(rgb_col))\n    if x_to is None:\n        x_to = np.linspace(0, 1, numcol)\n        \n    if x_to.min() < x_from.min() or x_to.max() > x_from.max():\n        raise ValueError(\"intpalette: cannot interpolate; ranges x.to > ranges x.from\")\n        \n    outcol = np.zeros((numcol, 3))\n    for i in range(3):\n        outcol[:, i] = np.interp(x_to, x_from, rgb_col[:, i])\n    \n    outcol = np.clip(np.round(outcol), 0, 255).astype(int)\n    \n    # Convert RGB to hex strings to match R's output\n    colors = [\"#%02x%02x%02x\" % tuple(row) for row in outcol]\n    return colors\n\ndef shadepalette(n=100, endcol=\"red\", inicol=\"white\", interval=(0, 1)):\n    x_to = np.linspace(interval[0], interval[1], n)\n    return intpalette([inicol, endcol], n, x_to=x_to)\n\n# Example 1: shadepalette(n = 10, \"white\", \"black\")\n# Note: In R, the arguments are n=10, endcol=\"white\", inicol=\"black\"\nres1 = shadepalette(10, \"white\", \"black\")\nprint(res1)\n\n# Example 2: image(matrix(nrow = 1, ncol = 100, data = 1:100), \n#                  col = shadepalette(100, \"red\", \"blue\"), main = \"shadepalette\")", "score": 1.0, "script_id": "shape__rd_example__shadepalette_Rd", "n_calls": 0}

## Edit Examples
(none)

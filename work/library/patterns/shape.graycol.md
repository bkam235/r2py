---
id: shape.graycol
package: shape
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# shape.graycol

## Guidance
Translate R `graycol` (FunctionCall from shape) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "9a91e68c", "r_snippet": "graycol(10)", "py_snippet": "def graycol(n=100, interval=(0, 0.7)):\n    \"\"\"\n    Produces a sequence of grey colors.\n    R's graycol calls shadepalette which interpolates between white and black \n    within the specified interval.\n    \"\"\"\n    # In R, graycol(n, interval=c(0, 0.7)) interpolates from white (0) to black (1)\n    # but only uses the segment of the gradient defined by interval.\n    # Since it's a grey scale, we can simply map the interval [0, 0.7] to [1, 0] in luminosity.\n    \n    # Map the interval to a range of greys. \n    # R: inicol=\"white\" (1.0), endcol=\"black\" (0.0)\n    # interval [0, 0.7] means we take va", "score": 0.9241, "script_id": "auto"}

## Edit Examples
(none)

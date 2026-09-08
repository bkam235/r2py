---
id: farver.decode-colour
package: farver
confidence: tentative
seed: true
created: 2026-09-08
last_review: 2026-09-08
tie_count: 0
---

# farver.decode-colour

## Guidance
Translate R `decode_colour` (FunctionCall from farver) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "97c4f004", "r_snippet": "decode_colour(c('#43e1f6', 'steelblue', '#67ce9fe4'))", "py_snippet": "def decode_colour(colour, alpha=False, to=\"rgb\", white=\"D65\", na_value=None):\n    \"\"\"\n    Decodes colors into a specified color space.\n    R farver's decode_colour returns 0-255 for RGB and specific LCH values.\n    \"\"\"\n    # Convert colors to RGBA normalized (0-1) using matplotlib\n    # matplotlib.colors.to_rgba handles hex, named colors, and RGBA\n    rgba_list = [mcolors.to_rgba(c) for c in colour]\n    \n    if to.lower() == \"rgb\":\n        # R farver returns RGB as 0-255 integers\n        results = []\n        for rgba in rgba_list:\n            # Convert 0-1 float to 0-255 int\n            rgb_25", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

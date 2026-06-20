---
id: matplotlib.rgb-to-hex-import
package: 
confidence: tentative
seed: false
created: 2026-06-14
last_review: 2026-06-14
tie_count: 0
---

# matplotlib.rgb-to-hex-import

## Guidance
matplotlib.colors provides rgb2hex (not rgb_to_hex) to convert RGB tuples to hex color strings. Update the import and all call sites accordingly.

## Evidence
- d42c7e223bcd → score 0.067 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "from matplotlib.colors import rgb_to_hex", "new_code": "from matplotlib.colors import rgb2hex", "score_delta": 0.0667, "script_id": "d42c7e223bcd"}

---
id: graycol-colorfunc
package: 
confidence: tentative
seed: false
created: 2026-06-13
last_review: 2026-06-13
tie_count: 0
---

# graycol-colorfunc

## Guidance
R's graycol(n) from the shape package generates a grayscale colormap with n colors. In Python, use matplotlib.cm.get_cmap('gray') to retrieve the grayscale colormap and sample it at n evenly-spaced points between 0 and 1 using np.linspace(0, 1, n). Wrap with print() to match R's auto-print behavior.

## Evidence
- d42c7e223bcd → score 0.003 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "graycol(10)", "new_code": "print(matplotlib.cm.get_cmap('gray')(np.linspace(0, 1, 10)))", "score_delta": 0.0033, "script_id": "d42c7e223bcd"}

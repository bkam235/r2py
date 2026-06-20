---
id: filled-contour-levels
package: 
confidence: tentative
seed: false
created: 2026-06-07
last_review: 2026-06-07
tie_count: 0
---

# filled-contour-levels

## Guidance
When translating R's filled.contour() to matplotlib's contourf(), avoid explicitly passing non-monotonic or duplicate contour levels. Instead, pass an integer to let matplotlib automatically generate evenly-spaced levels, which avoids the 'Contour levels must be increasing' error.

## Evidence
- dd2e0ea0b08b → score 0.002 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "# Use contourf for filled contours\ncontour_levels = np.linspace(volcano.min(), volcano.max(), 20)\ncontourf = ax.contourf(volcano, levels=contour_levels, cmap=graycol)", "new_code": "# Use contourf for filled contours (let matplotlib choose levels automatically)\ncontourf = ax.contourf(volcano, levels=15, cmap=graycol)", "score_delta": 0.0025, "script_id": "dd2e0ea0b08b"}

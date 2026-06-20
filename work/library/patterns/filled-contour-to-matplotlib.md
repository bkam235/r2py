---
id: filled-contour-to-matplotlib
package: 
confidence: tentative
seed: false
created: 2026-06-07
last_review: 2026-06-08
tie_count: 1
---

# filled-contour-to-matplotlib

## Guidance
R's filled.contour() creates a filled contour plot. Translate to matplotlib's contourf() method, mapping the 'color' parameter to 'cmap', 'asp' to 'aspect', and 'main' to set_title(). The empty try-except block must be replaced with actual plotting code to avoid syntax error.

## Evidence
- dd2e0ea0b08b → score 0.167 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)

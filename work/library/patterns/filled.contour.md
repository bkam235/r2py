---
id: filled.contour
package: shape
confidence: tentative
seed: false
created: 2026-06-19
last_review: 2026-06-19
tie_count: 0
---

# filled.contour

## Guidance
Translate to `plt.contourf` using a `ListedColormap`. Transpose the matrix (`Z.T`) and call `plt.gca().invert_yaxis()` to align with R's coordinate system.

Use plt.contourf with a transposed input matrix, plt.gca().set_aspect(1) for 'asp = 1', and plt.gca().invert_yaxis() to match R's coordinate system.

Translate to `plt.contourf()`. Use `volcano.T` (transpose) to match R's orientation and `plt.gca().set_aspect('equal')` to mimic `asp = 1`.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)

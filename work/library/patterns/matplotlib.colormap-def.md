---
id: matplotlib.colormap-def
package: 
confidence: tentative
seed: false
created: 2026-06-11
last_review: 2026-06-11
tie_count: 0
---

# matplotlib.colormap-def

## Guidance
When translating R's filled.contour with a color parameter, define the colormap before use. R's graycol is typically a grayscale colormap; in matplotlib, use plt.cm.gray or create a ListedColormap from grayscale values.

## Evidence
- d42c7e223bcd → score 0.108 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)

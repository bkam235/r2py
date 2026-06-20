---
id: image-graycol-colormap
package: 
confidence: tentative
seed: false
created: 2026-06-14
last_review: 2026-06-14
tie_count: 0
---

# image-graycol-colormap

## Guidance
R's image() with graycol() palette should translate to matplotlib's imshow() with ListedColormap directly from the graycol output (which returns hex color strings), not by processing them again through plt.cm.gray().

## Evidence
- d42c7e223bcd → score 0.184 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "files", "old_code": "im = ax.imshow(data, aspect='auto', cmap=plt.cm.colors.ListedColormap([plt.cm.gray(i/100) for i in graycol(100)]), origin='lower', interpolation='nearest')", "new_code": "im = ax.imshow(data, aspect='auto', cmap=ListedColormap(graycol(100)), origin='lower', interpolation='nearest')", "score_delta": 0.1837, "script_id": "d42c7e223bcd"}

---
id: graphics.image-to-imshow
package: 
confidence: tentative
seed: false
created: 2026-06-14
last_review: 2026-06-14
tie_count: 2
---

# graphics.image-to-imshow

## Guidance
R's image() function creates a heatmap visualization of a matrix. Translate to matplotlib's plt.imshow() with the matrix as a numpy array, col parameter to cmap, and main to plt.title(). Save the figure to match R's default PNG output behavior.

## Evidence
- d42c7e223bcd → score 0.025 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "pass", "new_code": "plt.imshow(np.array([[i for i in range(1, 101)]]), cmap=plt.cm.gray, aspect='auto')\nplt.title('greycol,graycol')\nplt.colorbar()\nplt.savefig('_r2py_plot_001.png')\nplt.close()", "score_delta": 0.0245, "script_id": "d42c7e223bcd"}

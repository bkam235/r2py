---
id: matplotlib.filled-contour-with-data
package: 
confidence: tentative
seed: true
created: 2026-06-08
last_review: 2026-06-08
tie_count: 0
---

# matplotlib.filled-contour-with-data

## Guidance
The `filled.contour()` function in R requires the data to be available in the execution context. In Python with matplotlib, we must ensure the dataset (volcano) is defined before calling `plt.contourf()`. Include the full volcano dataset as a numpy array before creating the plot.

**Critical: transpose the data matrix.** R's `filled.contour(z)` treats `z` as column-major: columns map to the x-axis, rows to the y-axis. Matplotlib's `contourf(z)` is row-major: rows map to the x-axis. To match R's orientation, pass `z.T` (the transpose). Without this, the plot will be rotated 90 degrees.

## Evidence
- dd2e0ea0b08b → score 0.005 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "plt.figure(figsize=(8, 10))\nplt.contourf(volcano, levels=15, cmap='gray')\nplt.colorbar()\nplt.title('greycol,graycol')\nplt.gca().set_aspect('equal')\nplt.show()", "new_code": "volcano = np.array([[100, 100, 101, 101, 101, 101, 101, 100, 100, 100, 101, 101, 102, 102, 102, 102, 103, 104, 103, 102, 101, 101, 102, 103, 104, 104, 105, 107, 107, 107, 108, 108, 110, 110, 110, 110, 110, 110, 110, 110, 108, 108, 108, 107, 107, 108, 108, 108, 108, 108, 107, 107, 107, 107, 106, 106,", "score_delta": 0.0051, "script_id": "dd2e0ea0b08b"}

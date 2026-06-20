---
id: r-matrix-to-numpy-array
package: 
confidence: tentative
seed: false
created: 2026-06-14
last_review: 2026-06-14
tie_count: 0
---

# r-matrix-to-numpy-array

## Guidance
In R, matrices are a fundamental data type. In Python, when translating R matrices passed to functions expecting array-like operations (especially transpose .T), wrap list representations with np.array() to create NumPy arrays that support these operations.

## Evidence
- d42c7e223bcd → score 0.501 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "71b1244c", "r_snippet": "filled.contour(volcano, color = graycol, asp = 1, main = \"greycol,graycol\")", "py_snippet": "# filled.contour(volcano, color = graycol, asp = 1, main = \"greycol,graycol\")\nplt.figure()\n# R's filled.contour and image treat the matrix differently than imshow.\n# We transpose to match R's visual orientation for the volcano dataset.\nplt.contourf(volcano.T, cmap=ListedColormap(graycol(100)))\nplt.gca().set_aspect('equal')\nplt.title(\"greycol,graycol\")\nplt.show()", "score": 0.8043, "script_id": "d42c7e223bcd"}

## Edit Examples
- {"failure_class": "stdout", "old_code": "contourf = ax.contourf(volcano.T, cmap=LinearSegmentedColormap.from_list(\"graycol\", graycol(100)))", "new_code": "contourf = ax.contourf(np.array(volcano).T, cmap=LinearSegmentedColormap.from_list(\"graycol\", graycol(100)))", "score_delta": 0.5014, "script_id": "d42c7e223bcd"}

---
id: r.builtin-dataset-to-array
package: 
confidence: tentative
seed: false
created: 2026-06-13
last_review: 2026-06-13
tie_count: 0
---

# r.builtin-dataset-to-array

## Guidance
R's built-in datasets like 'volcano' are automatically available but must be explicitly defined in Python. Convert R dataset references to numpy arrays or pandas dataframes before use in visualization functions.

## Evidence
- d42c7e223bcd → score 0.353 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "71b1244c", "r_snippet": "filled.contour(volcano, color = graycol, asp = 1, main = \"greycol,graycol\")", "py_snippet": "# filled.contour(volcano, color = graycol, asp = 1, main = \"greycol,graycol\")\nplt.figure()\n# R's filled.contour and image treat the matrix differently than imshow.\n# We transpose to match R's visual orientation for the volcano dataset.\nplt.contourf(volcano.T, cmap=ListedColormap(graycol(100)))\nplt.gca().set_aspect('equal')\nplt.title(\"greycol,graycol\")\nplt.show()", "score": 0.8043, "script_id": "d42c7e223bcd"}

## Edit Examples
(none)

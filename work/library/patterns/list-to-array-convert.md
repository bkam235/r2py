---
id: list-to-array-convert
package: 
confidence: tentative
seed: false
created: 2026-06-14
last_review: 2026-06-14
tie_count: 0
---

# list-to-array-convert

## Guidance
When R data structures (like volcano matrix) are loaded as Python lists instead of numpy arrays, convert them to numpy arrays before performing array operations like transpose (.T).

## Evidence
- d42c7e223bcd → score 0.318 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "71b1244c", "r_snippet": "filled.contour(volcano, color = graycol, asp = 1, main = \"greycol,graycol\")", "py_snippet": "# filled.contour(volcano, color = graycol, asp = 1, main = \"greycol,graycol\")\nplt.figure()\n# R's filled.contour and image treat the matrix differently than imshow.\n# We transpose to match R's visual orientation for the volcano dataset.\nplt.contourf(volcano.T, cmap=ListedColormap(graycol(100)))\nplt.gca().set_aspect('equal')\nplt.title(\"greycol,graycol\")\nplt.show()", "score": 0.8043, "script_id": "d42c7e223bcd"}

## Edit Examples
- {"failure_class": "stdout", "old_code": "contourf = ax.contourf(volcano.T, cmap=cmap, aspect='auto')", "new_code": "contourf = ax.contourf(np.array(volcano).T, cmap=cmap, aspect='auto')", "score_delta": 0.318, "script_id": "d42c7e223bcd"}

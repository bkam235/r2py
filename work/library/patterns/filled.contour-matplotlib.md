---
id: filled.contour-matplotlib
package: 
confidence: confirmed
seed: true
created: 2026-06-07
last_review: 2026-06-20
tie_count: 4
---

# filled.contour-matplotlib

## Guidance
Translate R's filled.contour() to matplotlib's contourf(). The R function creates a filled contour plot; in Python, use ax.contourf() with appropriate colormaps and aspect ratio settings.

**Critical: transpose the data matrix.** R's `filled.contour(z)` treats `z` as column-major: columns map to the x-axis, rows to the y-axis. Matplotlib's `contourf(z)` is row-major: rows map to the x-axis. To match R's orientation, pass `z.T` (the transpose). Without this, the plot will be rotated 90 degrees.

## Evidence
- dd2e0ea0b08b → score 0.167 (path: exact, variable: )
- d42c7e223bcd → score 0.138 (path: exact, variable: )
- d42c7e223bcd → score 0.138 (path: exact, variable: )
- d42c7e223bcd → score 0.505 (path: exact, variable: )
- d42c7e223bcd → score 0.318 (path: exact, variable: )
- d42c7e223bcd → score 0.505 (path: exact, variable: )
- d42c7e223bcd → score 0.346 (path: exact, variable: )
- d42c7e223bcd → score 0.470 (path: exact, variable: )

## Contradictions
- d42c7e223bcd/: score regressed to 0.000
- d42c7e223bcd/: score regressed to 0.133
- d42c7e223bcd/: score regressed to 0.000
- d42c7e223bcd/: score regressed to 0.632
- d42c7e223bcd/: score regressed to 0.280

## Translation Examples
- {"r_hash": "80efd3fe", "r_snippet": "chunk(complex(1e7))", "py_snippet": "# chunk(complex(1e7))\ndata_complex = np.empty(10**7, dtype=np.complex128)\nprint(format_ri_list(chunk(data_complex)))", "score": 1.0, "script_id": "ca1440d6104b"}
- {"r_hash": "72e823b4", "r_snippet": "  chunk(raw(1e7))", "py_snippet": "# chunk(raw(1e7))\ndata_raw = np.empty(10**7, dtype=np.uint8)\nprint(format_ri_list(chunk(data_raw)))", "score": 1.0, "script_id": "ca1440d6104b"}
- {"r_hash": "36c2885a", "r_snippet": "  chunk(raw(1e7), length=3)", "py_snippet": "# chunk(raw(1e7), length=3)\nprint(format_ri_list(chunk(data_raw, length_out=3)))", "score": 1.0, "script_id": "ca1440d6104b"}

## Edit Examples
- {"failure_class": "syntax", "old_code": "try:\n    \nexcept:\n    pass", "new_code": "# Create filled contour plot\nfig, ax = plt.subplots(figsize=(10, 8))\ncontourf = ax.contourf(volcano, cmap='gray', aspect='equal')\nax.set_aspect('equal')\nax.set_title(\"greycol,graycol\")\nplt.colorbar(contourf, ax=ax)\nplt.show()", "score_delta": 0.1667, "script_id": "dd2e0ea0b08b"}
- {"failure_class": "stdout", "old_code": "contourf = ax.contourf(volcano.T, cmap=mcolors.ListedColormap(colors), levels=20)", "new_code": "volcano_array = np.array(volcano)\ncontourf = ax.contourf(volcano_array.T, cmap=mcolors.ListedColormap(colors), levels=20)", "score_delta": 0.5048, "script_id": "d42c7e223bcd"}
- {"failure_class": "stdout", "old_code": "ax.contourf(volcano.T, cmap=cmap, levels=20)", "new_code": "ax.contourf(np.array(volcano).T, cmap=cmap, levels=20)", "score_delta": 0.5048, "script_id": "d42c7e223bcd"}
- {"failure_class": "stdout", "old_code": "# Create filled contour plot\nfig, ax = plt.subplots(figsize=(10, 8))\ncolors = graycol(100)\ncontourf = ax.contourf(volcano.T, levels=20, cmap=LinearSegmentedColormap.from_list(\"graycol\", colors))", "new_code": "# Create filled contour plot\nfig, ax = plt.subplots(figsize=(10, 8))\nvolcano_array = np.array(volcano)\ncolors = graycol(100)\ncontourf = ax.contourf(volcano_array.T, levels=20, cmap=LinearSegmentedColormap.from_list(\"graycol\", colors))", "score_delta": 0.47, "script_id": "d42c7e223bcd"}
- {"failure_class": "stdout", "old_code": "contourf = ax.contourf(volcano.T, colors=graycol(20), levels=20)", "new_code": "volcano_array = np.array(volcano)\ncontourf = ax.contourf(volcano_array.T, cmap=matplotlib.colors.ListedColormap(graycol(20)), levels=20)", "score_delta": 0.346, "script_id": "d42c7e223bcd"}
- {"failure_class": "stdout", "old_code": "# Create filled contour plot\ncolors = graycol(100)\ncmap = ListedColormap(colors)\n\nfig, ax = plt.subplots(figsize=(10, 8))\n# Transpose volcano to match R's column-major to row-major conversion\ncontourf = ax.contourf(volcano.T, cmap=cmap, aspect='equal')\nax.set_aspect('equal')\nax.set_title(\"greycol,gr", "new_code": "# Create filled contour plot\ncolors = graycol(100)\ncmap = ListedColormap(colors)\n\nvolcano_array = np.array(volcano)\nfig, ax = plt.subplots(figsize=(10, 8))\n# Transpose volcano to match R's column-major to row-major conversion\ncontourf = ax.contourf(volcano_array.T, cmap=cmap, aspect='equal')\nax.set_", "score_delta": 0.3184, "script_id": "d42c7e223bcd"}

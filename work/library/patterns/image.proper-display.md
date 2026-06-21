---
id: image.proper-display
package: 
confidence: confirmed
seed: true
created: 2026-06-07
last_review: 2026-06-14
tie_count: 0
---

# image.proper-display

## Guidance
**Critical: transpose the data matrix.** R's `image(z)` treats `z` as column-major: columns map to the x-axis, rows to the y-axis. Matplotlib's `imshow(z)` is row-major: rows map to the x-axis. To match R's orientation, pass `z.T` (the transpose) to `imshow()`. Without this, the plot will be rotated 90 degrees.

Translate R's `image()` to `plt.imshow()` with the appropriate colormap and `aspect='auto'`.

## Evidence
- dd2e0ea0b08b → score 0.023 (path: exact, variable: )
- d42c7e223bcd → score 0.026 (path: exact, variable: )

## Contradictions
- d42c7e223bcd/: score regressed to 0.225

## Translation Examples
- {"r_hash": "36ba7845", "r_snippet": "x <- c(\"bernard\", \"bÃ©rÃ©nice\", \"bÃ©atrice\", \"boris\")", "py_snippet": "x = [\"bernard\", \"bÃ©rÃ©nice\", \"bÃ©atrice\", \"boris\"]", "score": 1.0, "script_id": "021894dec169"}
- {"r_hash": "4044fd95", "r_snippet": "x <- list(x = c(1:100, NA, 1000), na.rm = TRUE, trim = 0.9)", "py_snippet": "x = {\n    \"x\": list(range(1, 101)) + [None, 1000],\n    \"na.rm\": True,\n    \"trim\": 0.9\n}", "score": 1.0, "script_id": "ca3c7c4facac"}
- {"r_hash": "f95e96e1", "r_snippet": "row.match(x,tab)", "py_snippet": "print(row_match(x=x, table=tab))", "score": 1.0, "script_id": "c4881a63292b"}

## Edit Examples
- {"failure_class": "graphics", "old_code": "# Create the matrix (1x100 with values 1-100)\ndata_matrix = np.arange(1, 101).reshape(1, 100)\n\n# Create grayscale colormap with 100 levels\n# graycol(100) generates 100 shades from black to white\ncmap = plt.cm.gray\ncolors = [cmap(i / 99) for i in range(100)]\n\n# Display the image\nplt.figure()\nplt.imsh", "new_code": "# Create the matrix (1x100 with values 1-100)\ndata_matrix = np.arange(1, 101).reshape(1, 100)\n\n# Create grayscale colormap with 100 levels\n# graycol(100) generates 100 shades from black to white\ndef graycol(n):\n    \"\"\"Generate n shades of gray from white to black as hex color codes.\"\"\"\n    return ['", "score_delta": 0.0233, "script_id": "dd2e0ea0b08b"}
- {"failure_class": "stdout", "old_code": "pass", "new_code": "plt.imshow(np.array([[i for i in range(1, 101)]]).T, cmap=plt.cm.gray, aspect='auto')\nplt.title('greycol,graycol')\nplt.colorbar()\nplt.savefig('_r2py_plot_001.png')\nplt.close()", "score_delta": 0.026, "script_id": "d42c7e223bcd"}

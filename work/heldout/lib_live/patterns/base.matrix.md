---
id: base.matrix
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.matrix

## Guidance
Translate R `matrix` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "3a5b137a", "r_snippet": "    img <- matrix(1:16/16, 4)", "py_snippet": "    img = np.arange(1, 17).reshape(4, 4, order='F') / 16.0\n    \n    # dataURI(writePNG(img), \"image/png\")\n    # r2py:entity:dataURI_2", "score": 1.0, "script_id": "base64enc__rd_example__dataURI_Rd", "n_calls": 1}
- {"r_hash": "64d46008", "r_snippet": "a <- list(matrix(1:4, ncol=2), matrix(1:6, ncol=2))", "py_snippet": "a = [np.arange(1, 5).reshape(2, 2), np.arange(1, 7).reshape(3, 2)]", "score": 1.0, "script_id": "reshape2__rd_example__melt_list_Rd", "n_calls": 1}
- {"r_hash": "875972a9", "r_snippet": "m <- matrix(\n  c(0, 0, 1, 1,\n    0, 1, 1, 1,\n    1, 1, 0, 0,\n    0, 0, 0.8, 0),\n  4, 4, byrow = TRUE\n)", "py_snippet": "m = np.array([\n    [0, 0, 1, 1],\n    [0, 1, 1, 1],\n    [1, 1, 0, 0],\n    [0, 0, 0.8, 0]\n])", "score": 1.0, "script_id": "isoband__vignette__isoband1_s5", "n_calls": 1}

## Edit Examples
- {"failure_class": "data_output", "old_code": "def writePNG(image, target=None):\n    # Simplified writePNG to match the use case of returning raw bytes\n    img = Image.fromarray((image * 255).astype(np.uint8), mode='L')\n    buf = io.BytesIO()\n    img.save(buf, format=\"PNG\")\n    return buf.getvalue()\n\n# Main script execution\ndata_raw = bytes(range(1, 11))\n\n    img = np.arange(1, 17).reshape(4, 4) / 16.0", "new_code": "    img = np.arange(1, 17).reshape(4, 4, order='F') / 16.0\n    \n    # dataURI(writePNG(img), \"image/png\")\n    # r2py:entity:dataURI_2", "score_delta": 0.75, "script_id": "base64enc__rd_example__dataURI_Rd", "r_snippet": "    img <- matrix(1:16/16, 4)", "functions": ["base::matrix"]}

---
id: base.matrix
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.matrix

## Guidance
Translate R `matrix` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "3a5b137a", "r_snippet": "    img <- matrix(1:16/16, 4)", "py_snippet": "    import PIL\n    # img <- matrix(1:16/16, 4) \n    # R fills by column: [1, 5, 9, 13], [2, 6, 10, 14]...", "score": 1.0, "script_id": "base64enc__rd_example__dataURI_Rd.R", "n_calls": 1}
- {"r_hash": "23dc89ed", "r_snippet": "m <- matrix(c(0, 0, 0, 0, 0, 0,\n              0, 2, 2, 2, 2, 0,\n              0, 2, 0, 0, 2, 0,\n              0, 2, 0, 0, 2, 0,\n              0, 2, 2, 2, 2, 0,\n              0, 0, 0, 0, 0, 0), 6, 6, byrow = TRUE)", "py_snippet": "m = np.array([\n    [0, 0, 0, 0, 0, 0],\n    [0, 2, 2, 2, 2, 0],\n    [0, 2, 0, 0, 2, 0],\n    [0, 2, 0, 0, 2, 0],\n    [0, 2, 2, 2, 2, 0],\n    [0, 0, 0, 0, 0, 0]", "score": 1.0, "script_id": "isoband__rd_example__plot_iso_Rd.R", "n_calls": 1}

## Edit Examples
(none)

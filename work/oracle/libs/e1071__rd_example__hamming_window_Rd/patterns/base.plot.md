---
id: base.plot
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.plot

## Guidance
Translate R `plot` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "015a64cc", "r_snippet": "plot(c_binded)", "py_snippet": "    # Approximate vertical concatenation of layouts\n    combined_data = np.vstack([gt1[\"data\"], gt2[\"data\"]])\n    combined_heights = gt1[\"heights\"] + gt2[\"heights\"]\n    combined_widths = gt1[\"widths\"] if size == \"first\" else gt2[\"widths\"]\n    return {\"data\": combined_data, \"heights\": combined_heights, \"widths\": combined_widths}\n\n# Execution\nc_binded = cbind(mat_gt, col_gt, size=\"first\")\n\n# Visualizing c_binded\nfig, ax = plt.subplots()\nax.set_xlim(0, 3)", "score": 1.0, "script_id": "gtable__rd_example__bind_Rd.R", "n_calls": 1}
- {"r_hash": "03ca6155", "r_snippet": "plot(r_binded)", "py_snippet": "ax.set_ylim(0, 2)\nax.add_patch(patches.Rectangle((0, 1), 1, 1, color=\"red\")) # mat_gt[0,0]\nax.add_patch(patches.Circle((1.5, 1.5), 0.5, color=\"blue\")) # mat_gt[0,1]\nax.add_line(plt.Line2D([0, 1], [0, 1], color=\"black\")) # mat_gt[1,0]\nax.add_patch(patches.Rectangle((2, 1), 1, 1, color=\"red\")) # col_gt[0,0]\nax.add_patch(patches.Circle((2.5, 0.5), 0.5, color=\"blue\")) # col_gt[1,0]\nplt.show()\n\nr_binded = rbind(mat_gt, row_gt, size=\"last\")\n\n# Visualizing r_binded", "score": 1.0, "script_id": "gtable__rd_example__bind_Rd.R", "n_calls": 1}
- {"r_hash": "e227ff62", "r_snippet": "plot(tab)", "py_snippet": "print(tab_dim)\nplot_gtable(3, 3, tab_fills)", "score": 1.0, "script_id": "gtable__rd_example__gtable_add_cols_Rd.R", "n_calls": 1}

## Edit Examples
(none)

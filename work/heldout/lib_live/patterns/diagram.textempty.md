---
id: diagram.textempty
package: diagram
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# diagram.textempty

## Guidance
Translate R `textempty` (FunctionCall from diagram) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "247b13ab", "r_snippet": "  textempty(mid = runif(2), box.col = i, lab = LETTERS[i], cex = 2)", "py_snippet": "letters = list(\"ABCDEFGHIJKLMNOPQRSTUVWXYZ\")\n\nfor i in range(1, 11):\n    # runif(2) generates two random numbers between 0 and 1\n    mid_coords = np.random.uniform(0, 1, 2)\n    \n    # Store parameters to simulate textempty loop\n    data_list.append({\n        'x': mid_coords[0], \n        'y': mid_coords[1], \n        'lab': letters[i-1], \n        'col': str(i),\n        'cex': 2\n    })\n\nd = pd.DataFrame(data_list)\n\n# Translate textempty visuals using plotnine.\n# Since plotnine doesn't have a native \"text box\" background like diagram::textempty,\n# we use geom_label which provides a background box around the text.\ng = (\n    ggplot(d, aes(x='x', y='y', label='lab', fill='col')) \n    + geom_label(size=10) \n    + xlim(-0.1, 1.1) \n    + ylim(-0.1, 1.1) \n    + labs(title=\"textempty\") \n    + theme_minimal()\n)\n\nprint(g)", "score": 0.9333, "script_id": "diagram__rd_example__textempty_Rd", "n_calls": 1}

## Edit Examples
(none)

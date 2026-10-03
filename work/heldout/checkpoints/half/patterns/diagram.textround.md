---
id: diagram.textround
package: diagram
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# diagram.textround

## Guidance
Translate R `textround` (FunctionCall from diagram) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "67319937", "r_snippet": "    textround(mid = runif(2), col = i, \n              radx = 0.03, rady = 0.075,\n              lab = LETTERS[i], cex = 2)", "py_snippet": "letters = list(\"ABCDEFGHIJKLMNOPQRSTUVWXYZ\")\n\nfor i in range(1, 11):\n    # runif(2) generates two random numbers between 0 and 1\n    mid_x, mid_y = np.random.uniform(0, 1, 2)\n    \n    # Store parameters to simulate the loop's effect\n    data_list.append({\n        'x': mid_x, \n        'y': mid_y, \n        'lab': letters[i-1], \n        'col': str(i)\n    })\n\nd = pd.DataFrame(data_list)\n\n# Translate textround visuals using plotnine\n# radx and rady are approximated by using geom_text and a custom point/size logic\n# since plotnine doesn't have a native \"rounded text box\" like diagram::textround,\n# we use geom_text with a background shape or simply plot the text.\ng = (\n    ggplot(d, aes(x='x', y='y', color='col', label='lab')) \n    + geom_text(size=10) \n    + xlim(-0.1, 1.1) \n    + ylim(-0.1, 1.1) \n    + labs(title=\"textround\") \n    + theme_minimal()\n)\n\nprint(g)", "score": 0.9333, "script_id": "diagram__rd_example__textround_Rd", "n_calls": 1}

## Edit Examples
(none)

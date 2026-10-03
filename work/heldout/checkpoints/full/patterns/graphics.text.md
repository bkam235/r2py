---
id: graphics.text
package: graphics
confidence: tentative
seed: true
created: 2026-09-23
last_review: 2026-09-23
tie_count: 0
---

# graphics.text

## Guidance
Translate R `text` (FunctionCall from graphics) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "54074097", "r_snippet": "text(coordinates(N = 6), lab = LETTERS[1:6], cex = 2)", "py_snippet": "coords1 = get_coordinates(N=6)\ndf1 = pd.DataFrame({'x': coords1[:,0], 'y': coords1[:,1], 'lab': list(\"ABCDEF\")})\np1 = (ggplot(df1) + \n      geom_text(aes(x='x', y='y', label='lab'), size=20) + \n      labs(title=\"coordinates\") + \n      theme_void())\nprint(p1)\n\n# text(coordinates(N = 8, relsize = 0.5), lab = letters[1:8], cex = 2)", "score": 0.9333, "script_id": "diagram__rd_example__coordinates_Rd", "n_calls": 1}

## Edit Examples
(none)

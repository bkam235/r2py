---
id: graphics.matplot
package: graphics
confidence: tentative
seed: true
created: 2026-09-14
last_review: 2026-09-14
tie_count: 0
---

# graphics.matplot

## Guidance
Translate R `matplot` (FunctionCall from graphics) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "fe216375", "r_snippet": "matplot(log2(benchmark64.data[-1,1]/benchmark64.data[-1,])\n, pch=c(\"3\", \"6\", \"h\", \"s\", \"o\", \"a\")\n, xlab=\"tasks [last=session]\"\n, ylab=\"log2(relative speed) [bigger is better]\"\n)", "py_snippet": "# Extract values excluding the first row\nsubset_data = benchmark64_data.iloc[1:, :].values\nfirst_col = subset_data[:, 0]\nrelative_speed = np.log2(first_col[:, np.newaxis] / subset_data)\n\n# First plot\nplt.figure()\n# R pch=c(\"3\", \"6\", \"h\", \"s\", \"o\", \"a\") \n# Python approximations: '3'->'v', '6'->'^', 'h'->'H', 's'->'s', 'o'->'o', 'a'->'.'\nmarkers = ['v', '^', 'H', 's', 'o', '.']\nfor i in range(relative_speed.shape[1]):\n    plt.plot(range(1, relative_speed.shape[0] + 1), relative_speed[:, i], \n             marker=markers[i] if i < len(markers) else 'o', linestyle='None')\nplt.xlabel(\"tasks [last=se", "score": 0.9333, "script_id": "auto"}

## Edit Examples
(none)

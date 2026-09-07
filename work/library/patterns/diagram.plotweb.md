---
id: diagram.plotweb
package: diagram
confidence: tentative
seed: true
created: 2026-09-07
last_review: 2026-09-07
tie_count: 0
---

# diagram.plotweb

## Guidance
Translate R `plotweb` (FunctionCall from diagram) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "f8553f2c", "r_snippet": "plotweb(Rigaweb, main = \"Gulf of Riga food web\",\n        sub = \"mgC/m3/d\", val = TRUE)", "py_snippet": "def plotweb(matrix, main=\"plotweb\", sub=None, val=True, arr_col=None):\n    \"\"\"\n    Equivalent to diagram::plotweb in R.\n    \"\"\"\n    G = nx.DiGraph()\n    rows, cols = matrix.shape\n    \n    for i in range(rows):\n        for j in range(cols):\n            weight = matrix[i, j]\n            if weight != 0:\n                G.add_edge(i, j, weight=weight)\n    \n    pos = nx.spring_layout(G)\n    plt.figure()\n    \n    # Handle arrow colors\n    if arr_col is not None:\n        # arr_col is a matrix of colors corresponding to the matrix\n        edge_colors = []\n        for u, v in G.edges():\n            edg", "score": 0.9, "script_id": "auto"}

## Edit Examples
(none)

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
- {"r_hash": "8915b460", "r_snippet": "  textdiamond(mid = runif(2), col = i, radx = 0.1, rady = 0.05,\n              lab = LETTERS[i], cex = 2, angle = runif(1)*360)", "py_snippet": "for idx, row in data.iterrows():\n    # Create diamond shape using an Ellipse\n    diamond = Ellipse(\n        xy=(row['x'], row['y']),\n        width=0.2,  # radx * 2\n        height=0.1, # rady * 2\n        angle=row['angle'],\n        edgecolor=plt.cm.tab10(row['color']/10),\n        facecolor='none',\n        linewidth=2\n    )\n    ax.add_patch(diamond)\n    \n    # Add text label\n    ax.text(\n        row['x'], row['y'], \n        row['label'], \n        ha='center', va='center', \n        fontsize=14, \n        rotation=row['angle']\n    )\n\nplt.show()", "score": 0.9333, "script_id": "auto"}
- {"r_hash": "acc210a4", "r_snippet": "openplotmat(xlim = c(-0.1, 1.1), main = \"textdiamond\")", "py_snippet": "fig, ax = plt.subplots(figsize=(6, 6))\nax.set_xlim(-0.1, 1.1)\nax.set_ylim(-0.1, 1.1)\nax.set_title(\"textdiamond\")\nax.axis('off')", "score": 0.9333, "script_id": "auto"}
- {"r_hash": "f8553f2c", "r_snippet": "plotweb(Rigaweb, main = \"Gulf of Riga food web\",\n        sub = \"mgC/m3/d\", val = TRUE)", "py_snippet": "def plotweb(matrix, main=\"plotweb\", sub=None, val=True, arr_col=None):\n    \"\"\"\n    Equivalent to diagram::plotweb in R.\n    \"\"\"\n    G = nx.DiGraph()\n    rows, cols = matrix.shape\n    \n    for i in range(rows):\n        for j in range(cols):\n            weight = matrix[i, j]\n            if weight != 0:\n                G.add_edge(i, j, weight=weight)\n    \n    pos = nx.spring_layout(G)\n    plt.figure()\n    \n    # Handle arrow colors\n    if arr_col is not None:\n        # arr_col is a matrix of colors corresponding to the matrix\n        edge_colors = []\n        for u, v in G.edges():\n            edg", "score": 0.9, "script_id": "auto"}

## Edit Examples
(none)

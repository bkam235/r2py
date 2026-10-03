---
id: diagram.openplotmat
package: diagram
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# diagram.openplotmat

## Guidance
Translate R `openplotmat` (FunctionCall from diagram) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "7e39c2bd", "r_snippet": "openplotmat(main = \"coordinates\")", "py_snippet": "def get_coordinates(N=None, pos=None, relsize=1, hor=True):\n    if pos is not None:\n        # Handle pos = c(rows, cols, ...) layout\n        rows, cols = pos[0], pos[1]\n        coords = []\n        for r in range(rows):\n            for c in range(cols):\n                coords.append((c, -r))\n        # If pos has a 3rd element (like 3 in the last example), \n        # it typically handles specific layout shifts in R; \n        # here we implement a basic grid based on the first two.\n        return np.array(coords)\n    \n    if N is not None:\n        # Default circle layout for N elements\n        theta = np.linspace(0, 2*np.pi, N, endpoint=False)\n        return np.column_stack([np.cos(theta), np.sin(theta)]) * relsize\n\n# --- Section 1 ---\n# openplotmat(main = \"coordinates\")\n# text(coordinates(N = 6), lab = LETTERS[1:6], cex = 2)", "score": 0.9333, "script_id": "diagram__rd_example__coordinates_Rd", "n_calls": 0}
- {"r_hash": "1169f3e8", "r_snippet": "openplotmat(xlim = c(-0.1, 1.1), col = \"lightgrey\", main = \"textempty\")", "py_snippet": "# Initialize plotting area (approximating openplotmat)\n# plotnine is declarative; we will build a dataframe for the loop\ndata_list = []", "score": 0.9333, "script_id": "diagram__rd_example__textempty_Rd", "n_calls": 0}
- {"r_hash": "dc41c34b", "r_snippet": "openplotmat(xlim = c(-0.1, 1.1), main = \"textround\")", "py_snippet": "# Initialize plotting area (approximating openplotmat)\n# plotnine is declarative; we will build a dataframe for the loop\ndata_list = []", "score": 0.9333, "script_id": "diagram__rd_example__textround_Rd", "n_calls": 0}

## Edit Examples
(none)

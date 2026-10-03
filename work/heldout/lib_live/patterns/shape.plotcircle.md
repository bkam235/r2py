---
id: shape.plotcircle
package: shape
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# shape.plotcircle

## Guidance
Translate R `plotcircle` (FunctionCall from shape) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "7407a60d", "r_snippet": "plotcircle(mid = c(0.5, 0.5), r = 0.25, from = 0, to = 3*pi/2,\n           arrow = TRUE, arr.pos = 0.5, col = \"red\")", "py_snippet": "def get_circle_data(mid, r, from_rad, to_rad, arrow=False, arr_pos=0.5):\n    t = np.linspace(from_rad, to_rad, 100)\n    x = mid[0] + r * np.cos(t)\n    y = mid[1] + r * np.sin(t)\n    df = pd.DataFrame({'x': x, 'y': y})\n    if arrow:\n        # Calculate point at arr_pos (relative to arc length)\n        idx = int(len(t) * arr_pos)\n        # Simple arrow head approximation using a point or custom logic\n        # Plotnine handles lines; arrow heads are typically handled by matplotlib\n        pass \n    return df\n\nd1_red = get_circle_data(mid=(0.5, 0.5), r=0.25, from_rad=0, to_rad=3*np.pi/2)", "score": 0.9333, "script_id": "shape__rd_example__plotcircle_Rd", "n_calls": 0}

## Edit Examples
(none)

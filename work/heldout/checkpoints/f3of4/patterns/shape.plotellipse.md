---
id: shape.plotellipse
package: shape
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# shape.plotellipse

## Guidance
Translate R `plotellipse` (FunctionCall from shape) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "f8ee7aa9", "r_snippet": "plotellipse(mid = c(0.5, 0.5), rx = 0.2, ry = 0.2, \n           arrow = TRUE, arr.pos = 0.5, col = \"blue\")", "py_snippet": "def get_ellipse_data(mid, rx, ry, arrow=False, arr_pos=0.5):\n    t = np.linspace(0, 2 * np.pi, 100)\n    x = mid[0] + rx * np.cos(t)\n    y = mid[1] + ry * np.sin(t)\n    df = pd.DataFrame({'x': x, 'y': y})\n    return df\n\n# First Plot\n\nd1_blue = get_ellipse_data(mid=(0.5, 0.5), rx=0.2, ry=0.2)\nd1_red['color'] = 'red'\nd1_blue['color'] = 'blue'\nd1 = pd.concat([d1_red, d1_blue])", "score": 0.9333, "script_id": "shape__rd_example__plotcircle_Rd", "n_calls": 0}

## Edit Examples
(none)

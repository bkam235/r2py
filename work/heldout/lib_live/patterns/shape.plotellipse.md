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
- {"r_hash": "e37d90b8", "r_snippet": "plotellipse(rx = 0.8, ry = 0.3, angle = 60, col = \"blue\")", "py_snippet": "def get_ellipse_data(rx=1, ry=None, mid=(0, 0), dr=0.01, angle=0, from_val=-np.pi, to_val=np.pi):\n    if ry is None:\n        ry = rx\n    \n    if to_val < from_val:\n        to_val = 2 * np.pi + to_val\n    \n    t = np.arange(from_val, to_val + dr, dr)\n    if len(t) > 1 and t[-1] > to_val:\n        t = t[:-1]\n    if len(t) > 0:\n        t = np.append(t, to_val)\n    \n    # Remove duplicates if dr is very small\n    t = np.unique(t)\n\n    x = mid[0] + rx * np.cos(t)\n    y = mid[1] + ry * np.sin(t)\n    \n    if angle != 0:\n        ang_rad = np.radians(angle)\n        cosa = np.cos(ang_rad)\n        sina = np.sin(ang_rad)\n        dx = x - mid[0]\n        dy = y - mid[1]\n        x = mid[0] + cosa * dx - sina * dy\n        y = mid[1] + sina * dx + cosa * dy\n        \n    return pd.DataFrame({'x': x, 'y': y})\n\ndef rainbow(n):\n    return [f\"rgb({int(255 * (i/n))}, 0, {int(255 * (1 - i/n))})\" for i in range(n)] # Approximation\n\n# In plotnine, we build layers. We'll collect all data and plot once to emulate R's plotting.\nplot_layers = []\nall_data = []\n\n# emptyplot(c(-1, 1), main = \"plotellipse\")\n\nd1 = get_ellipse_data(rx=0.8, ry=0.3, angle=60)\nd1['color'] = 'blue'\nd1['type'] = 'fill'\nall_data.append(d1)\n\n# 2. plotellipse(rx = 1.0, ry = 0.6, angle = 0, from_val= pi, to = 2*pi, arrow = TRUE, ...)\n# Python handles arrows better with geom_segment or custom marks, \n# but for a direct translation of the visual result into a dataframe:", "score": 0.9333, "script_id": "shape__rd_example__plotellipse_Rd", "n_calls": 0}
- {"r_hash": "f8ee7aa9", "r_snippet": "plotellipse(mid = c(0.5, 0.5), rx = 0.2, ry = 0.2, \n           arrow = TRUE, arr.pos = 0.5, col = \"blue\")", "py_snippet": "def get_ellipse_data(mid, rx, ry, arrow=False, arr_pos=0.5):\n    t = np.linspace(0, 2 * np.pi, 100)\n    x = mid[0] + rx * np.cos(t)\n    y = mid[1] + ry * np.sin(t)\n    df = pd.DataFrame({'x': x, 'y': y})\n    return df\n\n# First Plot\n\nd1_blue = get_ellipse_data(mid=(0.5, 0.5), rx=0.2, ry=0.2)\nd1_red['color'] = 'red'\nd1_blue['color'] = 'blue'\nd1 = pd.concat([d1_red, d1_blue])", "score": 0.9333, "script_id": "shape__rd_example__plotcircle_Rd", "n_calls": 0}

## Edit Examples
(none)

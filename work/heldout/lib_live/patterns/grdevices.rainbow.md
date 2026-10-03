---
id: grdevices.rainbow
package: grDevices
confidence: tentative
seed: true
created: 2026-09-24
last_review: 2026-09-24
tie_count: 0
---

# grdevices.rainbow

## Guidance
Translate R `rainbow` from grDevices to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "bb2cb4b5", "r_snippet": "plotellipse(rx = 1.0, ry = 0.6, angle = 0, from = pi, to = 2*pi,\n            arrow = TRUE, arr.pos = seq(0.1, 0.5, by = 0.1),\n            arr.col = rainbow(5))", "py_snippet": "d2 = get_ellipse_data(rx=1.0, ry=0.6, angle=0, from_val=np.pi, to_val=2*np.pi)\nd2['color'] = 'black'\nd2['type'] = 'line'\nall_data.append(d2)\n# Arrow positions: seq(0.1, 0.5, by = 0.1) -> 0.1, 0.2, 0.3, 0.4, 0.5\narr_pos = np.arange(0.1, 0.6, 0.1)\narr_cols = rainbow(5)\nfor pos, col in zip(arr_pos, arr_cols):\n    idx = int(len(d2) * pos)\n    if idx < len(d2) - 1:\n        # Represent arrows as small segments for plotnine\n        arrow_df = pd.DataFrame({\n            'x': [d2.iloc[idx-1]['x'], d2.iloc[idx]['x']],\n            'y': [d2.iloc[idx-1]['y'], d2.iloc[idx]['y']],\n            'color': [col, col],\n            'type': ['arrow', 'arrow']\n        })\n        all_data.append(arrow_df)\n\n# 3. plotellipse(rx = 1.0, ry = 0.6, angle = 30, from_val= pi, to = 1.2*pi, col = \"red\")", "score": 0.9333, "script_id": "shape__rd_example__plotellipse_Rd", "n_calls": 2}

## Edit Examples
(none)

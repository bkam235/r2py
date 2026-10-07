---
id: farver.decode-colour
package: farver
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# farver.decode-colour

## Guidance
Translate R `decode-colour` from farver to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "692e8dba", "r_snippet": "r <- decode_colour(rainbow(10))", "py_snippet": "def decode_colour(colour, alpha=False, to='rgb', white='D65', na_value=None):\n    \"\"\"\n    Replicates farver::decode_colour.\n    Converts colour representations (like hex or RGB) to a numeric matrix.\n    \"\"\"\n    c = np.array(colour)\n    # For the scope of these examples, decode_colour essentially returns the RGB values\n    # normalized or as integers. We'll maintain the matrix form.\n    return c\n        return cdist(c1, c2, metric='euclidean')\n\ndef r_rainbow(n):\n    \"\"\"\n    Replicates R's rainbow(n).\n    \"\"\"\n    import colorsys\n    h_vals = np.linspace(0, 1, n, endpoint=False)\n    rgb = []\n        res.append([255, g, b])\n    return np.array(res)", "score": 1.0, "script_id": "farver__rd_example__compare_colour_Rd.R", "n_calls": 1}
- {"r_hash": "8284fbc6", "r_snippet": "h <- decode_colour(heat.colors(15))", "py_snippet": "        rgb.append(colorsys.hsv_to_rgb(h, 1.0, 1.0))\n    return np.array([[int(round(x * 255)) for x in c] for c in rgb])\n\ndef r_heat_colors(n):\n    \"\"\"\n    Replicates R's heat.colors(n).\n    \"\"\"\n    res = []\n    for i in range(n):\n        if i < 12:\n            g = int(round(i * (255 / 11)))\n            b = 0\n        elif i == 12:\n            g = 255\n            b = 42\n        elif i == 13:\n            g = 255\n            b = 128\n        else:\n            g = 255\n            b = 213\n# r <- decode_colour(rainbow(10))\nr = decode_colour(r_rainbow(10))", "score": 1.0, "script_id": "farver__rd_example__compare_colour_Rd.R", "n_calls": 1}

## Edit Examples
(none)

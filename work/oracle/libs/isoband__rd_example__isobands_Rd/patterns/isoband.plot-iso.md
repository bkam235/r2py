---
id: isoband.plot-iso
package: isoband
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# isoband.plot-iso

## Guidance
Translate R `plot-iso` from isoband to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "255f8d02", "r_snippet": "plot_iso(m, 0.5, 1.5)", "py_snippet": "def plot_iso(m, vlo, vhi, fill_lo=\"gray95\", fill_mid=\"gray50\", \n             fill_hi=\"black\", fill_band=\"cornsilk\", col_lo=\"black\", \n             col_hi=\"black\", newpage=True):\n    # Map R colors to Matplotlib compatible colors\n    color_map = {\n        \"gray95\": \"#F2F2F2\",\n        \"gray50\": \"#808080\",\n        \"black\": \"#000000\",\n        \"cornsilk\": \"#FFF8DC\"\n    }\n    \n    f_lo = color_map.get(fill_lo, fill_lo)\n    f_mid = color_map.get(fill_mid, fill_mid)\n    f_hi = color_map.get(fill_hi, fill_hi)\n    f_band = color_map.get(fill_band, fill_band)\n    c_lo = color_map.get(col_lo, col_lo)\n    c_hi = color_map.get(col_hi, col_hi)\n\n    rows, cols = m.shape\n    x = np.linspace(0, 1, cols)\n    y = np.linspace(1, 0, rows) # Y is reversed in the R source's grid logic\n    X, Y = np.meshgrid(x, y)\n\n    fig, ax = plt.subplots()\n\n    # Draw the band between vlo and vhi\n    ax.contourf(X, Y, m, levels=[vlo, vhi], colors=[f_band], alpha=1)\n    \n    # Draw the isolines at vlo and vhi\n    ax.contour(X, Y, m, levels=[vlo], colors=[c_lo])\n    ax.contour(X, Y, m, levels=[vhi], colors=[c_hi])\n\n    # Draw the points (grid nodes)\n    # Flatten m and determine colors based on thresholds\n    z_flat = m.flatten()\n    p_fill = []\n    p_col = []\n    for val in z_flat:\n        if val < vlo:\n            p_fill.append(f_lo)\n            p_col.append(\"black\")\n        elif val < vhi:\n            p_fill.append(f_mid)\n            p_col.append(f_mid)\n        else:\n            p_fill.append(f_hi)\n            p_col.append(\"black\")\n\n    ax.scatter(X.flatten(), Y.flatten(), c=p_fill, edgecolors=p_col, s=10, zorder=3)\n    \n    ax.set_aspect('equal')\n    ax.axis('off')\n    plt.show()", "score": 1.0, "script_id": "isoband__rd_example__plot_iso_Rd.R", "n_calls": 0}

## Edit Examples
(none)

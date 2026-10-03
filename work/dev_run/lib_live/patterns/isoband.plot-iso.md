---
id: isoband.plot-iso
package: isoband
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# isoband.plot-iso

## Guidance
Translate R `plot_iso` (FunctionCall from isoband) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "255f8d02", "r_snippet": "plot_iso(m, 0.5, 1.5)", "py_snippet": "x = np.arange(m.shape[1])\ny = np.arange(m.shape[0])\nX, Y = np.meshgrid(x, y)\n\n# plot_iso(m, 0.5, 1.5) suggests levels at 0.5 and 1.5\n# Note: 1.5 is outside the range of m (0-1), so it won't appear.\nlevels = [0.5, 1.5]\n\nplt.contourf(X, Y, m, levels=levels, extend='both')\nplt.colorbar()\nplt.show()", "score": 1.0, "script_id": "isoband__vignette__isoband1_s5", "n_calls": 0}

## Edit Examples
(none)

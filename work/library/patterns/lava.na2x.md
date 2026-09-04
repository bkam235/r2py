---
id: lava.na2x
package: lava
confidence: tentative
seed: true
created: 2026-09-04
last_review: 2026-09-04
tie_count: 0
---

# lava.na2x

## Guidance
Translate R `NA2x` (FunctionCall from lava) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "a4195739", "r_snippet": "NA2x(x2NA(c(1:10),5),5)##'", "py_snippet": "def NA2x(s, x=0):\n    \"\"\"\n    Translates to Python using pandas/numpy to replace NaNs with x.\n    \"\"\"\n    s_arr = np.array(s)\n    # Replace NaN values with x\n    res = np.where(np.isnan(s_arr), x, s_arr)\n    return res\n\n# Main script translation\n# R: x2NA(1:10, 1:5)\n\nres_x2na = x2NA(np.arange(1, 11), 5)\nprint(NA2x(res_x2na, 5))", "score": 0.9, "script_id": "auto"}

## Edit Examples
(none)

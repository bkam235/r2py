---
id: base.rep
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.rep

## Guidance
Translate R `rep` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "dcf0bc92", "r_snippet": "rep(1, 6) + 1", "py_snippet": "res = np.full(6, 1) + 1\nprint(res)\n\n# rep(1, 6) + 1:2\n# R recycling: 1:2 is [1, 2], repeated to [1, 2, 1, 2, 1, 2]", "score": 1.0, "script_id": "vctrs__vignette__type-size_s29.R", "n_calls": 1}
- {"r_hash": "a8085d91", "r_snippet": "rep(1, 6) + 1:2", "py_snippet": "res_1 = np.full(6, 1) + np.tile(np.arange(1, 3), 3)\nprint(res_1)\n\n# rep(1, 6) + 1:3", "score": 1.0, "script_id": "vctrs__vignette__type-size_s29.R", "n_calls": 1}

## Edit Examples
(none)

---
id: base.rep
package: base
confidence: tentative
seed: true
created: 2026-09-24
last_review: 2026-09-24
tie_count: 0
---

# base.rep

## Guidance
Translate R `rep` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "dcf0bc92", "r_snippet": "rep(1, 6) + 1", "py_snippet": "res = np.full(6, 1) + 1\nprint(res)\n\n# rep(1, 6) + 1:2\n# R recycling: 1:2 is [1, 2], repeated to [1, 2, 1, 2, 1, 2]", "score": 1.0, "script_id": "vctrs__vignette__type-size_s29", "n_calls": 1}

## Edit Examples
- {"failure_class": "side_effects", "old_code": "res1 = np.full(6, 1) + 1\n\n# rep(1, 6) + 1:2\n# R performs recycling: [1, 2, 1, 2, 1, 2]", "new_code": "res = np.full(6, 1) + 1\nprint(res)\n\n# rep(1, 6) + 1:2\n# R recycling: 1:2 is [1, 2], repeated to [1, 2, 1, 2, 1, 2]", "score_delta": 0.5, "script_id": "vctrs__vignette__type-size_s29", "r_snippet": "rep(1, 6) + 1", "functions": ["base::rep"]}
- {"failure_class": "side_effects", "old_code": "res2 = np.full(6, 1) + np.tile(np.arange(1, 3), 3)\n\n# rep(1, 6) + 1:3\n# R performs recycling: [1, 2, 3, 1, 2, 3]", "new_code": "res_1 = np.full(6, 1) + np.tile(np.arange(1, 3), 3)\nprint(res_1)\n\n# rep(1, 6) + 1:3\n# R recycling: 1:3 is [1, 2, 3], repeated to [1, 2, 3, 1, 2, 3]", "score_delta": 0.5, "script_id": "vctrs__vignette__type-size_s29", "r_snippet": "rep(1, 6) + 1:2", "functions": ["base::rep"]}
- {"failure_class": "side_effects", "old_code": "res3 = np.full(6, 1) + np.tile(np.arange(1, 4), 2)", "new_code": "res_2 = np.full(6, 1) + np.tile(np.arange(1, 4), 2)\nprint(res_2)", "score_delta": 0.5, "script_id": "vctrs__vignette__type-size_s29", "r_snippet": "rep(1, 6) + 1:3", "functions": ["base::rep"]}

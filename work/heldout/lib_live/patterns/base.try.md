---
id: base.try
package: base
confidence: tentative
seed: true
created: 2026-09-23
last_review: 2026-09-23
tie_count: 0
---

# base.try

## Guidance
Translate R `try` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e9e23fe4", "r_snippet": "try(x[[3]])", "py_snippet": "try:\n    # R: x[[3]] on a list with named elements often errors if index is out of bounds\n    # Python dicts error on integer keys if they don't exist\n    val = x[3]\nexcept Exception:\n    pass\n\n# chuck() consistently errors:", "score": 1.0, "script_id": "purrr__rd_example__chuck_Rd", "n_calls": 1}
- {"r_hash": "34f712cb", "r_snippet": "try(vec_cast(c(1, 1.5), integer()))", "py_snippet": "try:\n    vec_cast_with_result([1, 1.5], np.int32)\nexcept Exception:\n    pass\n\n# try(vec_cast(c(1, 2), logical()))", "score": 1.0, "script_id": "vctrs__rd_example__vec_cast_Rd", "n_calls": 2}

## Edit Examples
- {"failure_class": "side_effects", "old_code": "try:\n    print(x[\"y\"])\nexcept KeyError:\n    print(None)\n\ntry:\n    # Python dicts do not support integer indexing unless the keys are integers\n    print(x[3])\nexcept KeyError:\n    print(None)", "new_code": "try:\n    # R: x[[3]] on a list with named elements often errors if index is out of bounds\n    # Python dicts error on integer keys if they don't exist\n    val = x[3]\nexcept Exception:\n    pass\n\n# chuck() consistently errors:", "score_delta": 0.4231, "script_id": "purrr__rd_example__chuck_Rd", "r_snippet": "try(x[[3]])", "functions": ["base::try"]}

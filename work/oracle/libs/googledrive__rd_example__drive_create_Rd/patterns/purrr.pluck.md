---
id: purrr.pluck
package: purrr
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# purrr.pluck

## Guidance
Translate R `pluck` from purrr to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "46f0fc68", "r_snippet": "pluck(x, 1, attr_getter(\"obj_attr\"))  # From first object", "py_snippet": "x = [obj1, obj2]\n\n# pluck implementation for Python\ndef pluck(x, *indices, default=None):\n    res = x\n    for idx in indices:\n        try:\n            if callable(idx):\n                res = idx(res)\n            elif isinstance(res, (list, tuple)):\n                # R's pluck uses 1-based indexing\n            else:\n                res = res[idx]", "score": 1.0, "script_id": "purrr__rd_example__attr_getter_Rd.R", "n_calls": 0}
- {"r_hash": "26d15c49", "r_snippet": "pluck(x, 2, attr_getter(\"obj_attr\"))  # From second object", "py_snippet": "            return default\n    return res", "score": 1.0, "script_id": "purrr__rd_example__attr_getter_Rd.R", "n_calls": 0}

## Edit Examples
(none)

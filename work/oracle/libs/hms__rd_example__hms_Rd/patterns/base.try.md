---
id: base.try
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.try

## Guidance
Translate R `try` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e9e23fe4", "r_snippet": "try(x[[3]])", "py_snippet": "# and sometimes errors:\ntry:\n    # R: x[[3]] on a list with named elements often errors if index is out of bounds\n    # Python dicts error on integer keys if they don't exist\n    val = x[3]\nexcept Exception:\n    pass", "score": 1.0, "script_id": "purrr__rd_example__chuck_Rd.R", "n_calls": 1}
- {"r_hash": "393641d4", "r_snippet": "try(chuck(x, \"y\"))", "py_snippet": "def chuck(x, key):\n    # R's chuck() is a strict version of pluck()\n    # It must error if the key is missing\n    if key not in x:\n        raise KeyError(f\"key {key} not found\")\n    return x[key]\n\n# When indexing an element that doesn't exist `[[` sometimes returns NULL:\n# In R, x[[\"y\"]] for a list returns NULL without error.\n# Python dict.get() mimics this behavior.\nres_y = x.get(\"y\")\nprint(res_y) if res_y is not None else print(\"NULL\")\n\n\n# chuck() consistently errors:\ntry:", "score": 1.0, "script_id": "purrr__rd_example__chuck_Rd.R", "n_calls": 1}

## Edit Examples
(none)

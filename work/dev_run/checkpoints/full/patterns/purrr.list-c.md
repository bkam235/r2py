---
id: purrr.list-c
package: purrr
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# purrr.list-c

## Guidance
Translate R `list_c` (FunctionCall from purrr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "87d7ee5c", "r_snippet": "list_c(x1)", "py_snippet": "def list_c(x, ptype=None):\n    \"\"\"\n    Flatten a list into a vector.\n    Equivalent to R's list_c or unlist().\n    \"\"\"\n    # Convert list to a flat list of values\n    flat_list = []\n    for item in x.values() if isinstance(x, dict) else x:\n        if isinstance(item, (list, np.ndarray, pd.Series)):\n            flat_list.extend(item)\n        else:\n            flat_list.append(item)\n    return np.array(flat_list)\n\nprint(list_c(x1))", "score": 1.0, "script_id": "purrr__rd_example__list_c_Rd", "n_calls": 0}

## Edit Examples
(none)

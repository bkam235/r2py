---
id: lubridate.hms
package: lubridate
confidence: tentative
seed: true
created: 2026-09-22
last_review: 2026-09-22
tie_count: 0
---

# lubridate.hms

## Guidance
Translate R `hms` (FunctionCall from lubridate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "06821d22", "r_snippet": "hms(x)", "py_snippet": "def hms(*args, quiet=False, roll=False):\n    inputs = []\n    for arg in args:\n        if isinstance(arg, (list, np.ndarray, pd.Series)):\n            inputs.extend(arg)\n        else:\n            inputs.append(arg)\n            \n    return _parse_hms_logic(inputs, \"HMS\")\n\ndef format_r_vector(vec):\n    # Simulates R's print output for vectors: [1] \"val1\" \"val2\"\n    items = \" \".join([f'\"{str(x)}\"' for x in vec])\n    return f'[1] {items}'\n\n# Execution\n\nres_hms = hms(x)\nprint(format_r_vector(res_hms))", "score": 1.0, "script_id": "lubridate__rd_example__hms_Rd", "n_calls": 0}

## Edit Examples
(none)

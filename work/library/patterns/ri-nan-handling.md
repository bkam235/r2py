---
id: ri-nan-handling
package: 
confidence: tentative
seed: false
created: 2026-06-17
last_review: 2026-06-17
tie_count: 0
---

# ri-nan-handling

## Guidance
In the ri() function, maxindex should not be converted to int when it is NaN, since NaN cannot be converted to integer. Keep maxindex as a float (NaN) and let validation logic handle it with math.isnan() checks.

## Evidence
- ca1440d6104b → score 0.467 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "80efd3fe", "r_snippet": "chunk(complex(1e7))", "py_snippet": "# chunk(complex(1e7))\ndata_complex = np.empty(10**7, dtype=np.complex128)\nprint(format_ri_list(chunk(data_complex)))", "score": 1.0, "script_id": "ca1440d6104b"}

## Edit Examples
- {"failure_class": "syntax", "old_code": "def ri(from_val, to=None, maxindex=np.nan):\n    \"\"\"Range index object with validation.\"\"\"\n    if to is None:\n        x = [int(from_val), int(maxindex)]\n    else:\n        x = [int(from_val), int(to), int(maxindex)]", "new_code": "def ri(from_val, to=None, maxindex=np.nan):\n    \"\"\"Range index object with validation.\"\"\"\n    if to is None:\n        x = [int(from_val), maxindex]\n    else:\n        x = [int(from_val), int(to), maxindex]", "score_delta": 0.4672, "script_id": "ca1440d6104b"}

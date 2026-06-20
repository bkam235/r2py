---
id: bit.ri-nan-handling
package: 
confidence: tentative
seed: false
created: 2026-06-17
last_review: 2026-06-17
tie_count: 0
---

# bit.ri-nan-handling

## Guidance
When converting R's range index (ri) objects to Python, maxindex can be NA/NaN. Avoid calling int() on NaN values; instead, preserve NaN in the list and only convert numeric values to int.

## Evidence
- ca1440d6104b → score 0.467 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "80efd3fe", "r_snippet": "chunk(complex(1e7))", "py_snippet": "# chunk(complex(1e7))\ndata_complex = np.empty(10**7, dtype=np.complex128)\nprint(format_ri_list(chunk(data_complex)))", "score": 1.0, "script_id": "ca1440d6104b"}

## Edit Examples
- {"failure_class": "syntax", "old_code": "def ri(from_val, to=None, maxindex=np.nan):\n    \"\"\"Range index object with validation.\"\"\"\n    if to is None:\n        x = [int(from_val), int(maxindex)]\n    else:\n        x = [int(from_val), int(to), int(maxindex)]", "new_code": "def ri(from_val, to=None, maxindex=np.nan):\n    \"\"\"Range index object with validation.\"\"\"\n    if to is None:\n        x = [int(from_val), maxindex if math.isnan(maxindex) else int(maxindex)]\n    else:\n        x = [int(from_val), int(to), maxindex if math.isnan(maxindex) else int(maxindex)]", "score_delta": 0.4672, "script_id": "ca1440d6104b"}

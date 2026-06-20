---
id: bit.ri-nan-conversion
package: 
confidence: tentative
seed: false
created: 2026-06-16
last_review: 2026-06-16
tie_count: 0
---

# bit.ri-nan-conversion

## Guidance
When converting function arguments that may be NaN (used as sentinel values in R's bit package), preserve NaN values instead of forcing conversion to int, which raises ValueError. Check for NaN before integer conversion.

## Evidence
- ca1440d6104b → score 0.350 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "80efd3fe", "r_snippet": "chunk(complex(1e7))", "py_snippet": "# chunk(complex(1e7))\ndata_complex = np.empty(10**7, dtype=np.complex128)\nprint(format_ri_list(chunk(data_complex)))", "score": 1.0, "script_id": "ca1440d6104b"}

## Edit Examples
- {"failure_class": "syntax", "old_code": "def ri(from_val, to_val=None, maxindex=np.nan):\n    \"\"\"ri function from bit package\"\"\"\n    if to_val is None:\n        x = [int(from_val), int(maxindex)]\n    else:\n        x = [int(from_val), int(to_val), int(maxindex)]", "new_code": "def ri(from_val, to_val=None, maxindex=np.nan):\n    \"\"\"ri function from bit package\"\"\"\n    if to_val is None:\n        x = [int(from_val), maxindex if np.isnan(maxindex) else int(maxindex)]\n    else:\n        x = [int(from_val), int(to_val), maxindex if np.isnan(maxindex) else int(maxindex)]", "score_delta": 0.3502, "script_id": "ca1440d6104b"}

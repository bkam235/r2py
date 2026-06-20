---
id: nan-array-conversion-fix
package: 
confidence: tentative
seed: false
created: 2026-06-16
last_review: 2026-06-16
tie_count: 0
---

# nan-array-conversion-fix

## Guidance
When handling numpy array construction with NaN values that need to be int64 dtype, convert scalar values individually to int before array creation, keeping NaN separate to avoid dtype conversion errors.

## Evidence
- ca1440d6104b → score 0.245 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "def ri(from_val, to_val=None, maxindex=np.nan):\n    \"\"\"Create a range index object with validation.\"\"\"\n    if to_val is None:\n        x = np.array([from_val, maxindex], dtype=np.int64)\n    else:\n        x = np.array([from_val, to_val, maxindex], dtype=np.int64)\n    \n    if len(x) != 3:\n        raise", "new_code": "def ri(from_val, to_val=None, maxindex=np.nan):\n    \"\"\"Create a range index object with validation.\"\"\"\n    if to_val is None:\n        from_int = int(from_val)\n        to_int = int(maxindex) if not np.isnan(maxindex) else from_int\n    else:\n        from_int = int(from_val)\n        to_int = int(to_val", "score_delta": 0.245, "script_id": "ca1440d6104b"}

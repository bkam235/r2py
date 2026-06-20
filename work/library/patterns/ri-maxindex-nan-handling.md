---
id: ri-maxindex-nan-handling
package: 
confidence: tentative
seed: false
created: 2026-06-16
last_review: 2026-06-16
tie_count: 0
---

# ri-maxindex-nan-handling

## Guidance
When converting values to int32 array in the ri() function, handle np.nan separately since numpy cannot convert NaN to integer. Only convert finite numeric values to int, leaving NaN as-is.

## Evidence
- ca1440d6104b → score 0.077 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "def ri(from_val, to_val=None, maxindex=np.nan):\n    \"\"\"Create a range index object (ri).\"\"\"\n    \n    if to_val is None:\n        x = np.array([from_val, maxindex], dtype=np.int32)\n    else:\n        x = np.array([from_val, to_val, maxindex], dtype=np.int32)", "new_code": "def ri(from_val, to_val=None, maxindex=np.nan):\n    \"\"\"Create a range index object (ri).\"\"\"\n    \n    if to_val is None:\n        x = np.array([int(from_val), int(maxindex) if not np.isnan(maxindex) else maxindex])\n    else:\n        x = np.array([int(from_val), int(to_val), maxindex])", "score_delta": 0.0769, "script_id": "ca1440d6104b"}

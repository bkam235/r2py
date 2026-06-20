---
id: nan-safe-int-conversion
package: 
confidence: tentative
seed: false
created: 2026-06-16
last_review: 2026-06-16
tie_count: 0
---

# nan-safe-int-conversion

## Guidance
When converting values to int that may be NaN (missing values), check with pd.isna() first. Only convert to int if the value is not NaN; otherwise preserve the NaN to indicate a missing/unbounded value.

## Evidence
- ca1440d6104b → score 0.202 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "def ri(from_val, to=None, maxindex=np.nan):\n    \"\"\"Helper: creates a range index object with validation.\"\"\"\n    if to is None:\n        x = [int(from_val), int(maxindex)]\n    else:\n        x = [int(from_val), int(to), int(maxindex)]", "new_code": "def ri(from_val, to=None, maxindex=np.nan):\n    \"\"\"Helper: creates a range index object with validation.\"\"\"\n    if to is None:\n        x = [int(from_val), int(maxindex) if not pd.isna(maxindex) else maxindex]\n    else:\n        x = [int(from_val), int(to), int(maxindex) if not pd.isna(maxindex) else ", "score_delta": 0.2018, "script_id": "ca1440d6104b"}

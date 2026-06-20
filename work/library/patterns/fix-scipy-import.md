---
id: fix-scipy-import
package: 
confidence: tentative
seed: false
created: 2026-06-07
last_review: 2026-06-07
tie_count: 0
---

# fix-scipy-import

## Guidance
Remove invalid scipy.datasets._get_data import that causes ImportError. In modern scipy, datasets are accessed differently or through alternative sources.

## Evidence
- dd2e0ea0b08b → score 0.067 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "from scipy.datasets import _get_data", "new_code": "# from scipy.datasets import _get_data  # Not available in modern scipy; removed", "score_delta": 0.0667, "script_id": "dd2e0ea0b08b"}

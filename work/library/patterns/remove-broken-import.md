---
id: remove-broken-import
package: 
confidence: tentative
seed: false
created: 2026-06-09
last_review: 2026-06-09
tie_count: 0
---

# remove-broken-import

## Guidance
When a Python import fails (e.g., scipy.datasets.load_volcano doesn't exist), remove the broken import statement and rely on fallback data or computation instead. This unblocks the script execution so other entities can be evaluated.

## Evidence
- d42c7e223bcd → score 0.067 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "from scipy.datasets import load_volcano", "new_code": "# load_volcano not available in scipy.datasets; using fallback", "score_delta": 0.0667, "script_id": "d42c7e223bcd"}

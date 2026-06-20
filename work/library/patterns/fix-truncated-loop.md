---
id: fix-truncated-loop
package: 
confidence: tentative
seed: false
created: 2026-06-15
last_review: 2026-06-15
tie_count: 0
---

# fix-truncated-loop

## Guidance
Complete the truncated for loop in the finally block of with_locale context manager. The loop was cut off at 'for cat_nam' and needs to be fully written as 'for cat_name in old_locales:' with proper restoration logic.

## Evidence
- 021894dec169 → score 0.742 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "59c74ac3", "r_snippet": "suppressPackageStartupMessages(library(withr))", "py_snippet": "warnings.filterwarnings('ignore')", "score": 1.0, "script_id": "021894dec169"}

## Edit Examples
(none)

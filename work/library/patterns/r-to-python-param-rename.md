---
id: r-to-python-param-rename
package: 
confidence: tentative
seed: false
created: 2026-06-17
last_review: 2026-06-17
tie_count: 0
---

# r-to-python-param-rename

## Guidance
R uses partial argument matching and periods in parameter names (e.g., length.out). Python requires exact parameter names with underscores. When translating R function calls, replace period-separated parameter names with underscore equivalents (length.out → length_out) to match the Python function signature.

## Evidence
- ca1440d6104b → score 0.180 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "chunk(np.zeros(int(1e7), dtype=np.uint8), length=3)", "new_code": "chunk(np.zeros(int(1e7), dtype=np.uint8), length_out=3)", "score_delta": 0.1804, "script_id": "ca1440d6104b"}

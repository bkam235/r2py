---
id: arg-name-mismatch
package: 
confidence: tentative
seed: false
created: 2026-06-18
last_review: 2026-06-18
tie_count: 0
---

# arg-name-mismatch

## Guidance
When calling Python functions translated from R, verify argument names match the function signature. R's `...` (dots) parameters are expanded as keyword arguments, so parameter names must correspond exactly to the Python function's formal parameters.

## Evidence
- ca1440d6104b → score 0.059 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "chunks(from_=1, to=10, by=3)", "new_code": "chunks(from_val=1, to=10, by=3)", "score_delta": 0.059, "script_id": "ca1440d6104b"}

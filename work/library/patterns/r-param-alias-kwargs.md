---
id: r-param-alias-kwargs
package: 
confidence: tentative
seed: false
created: 2026-06-17
last_review: 2026-06-17
tie_count: 0
---

# r-param-alias-kwargs

## Guidance
When R functions accept parameter names like 'length' that don't match Python conventions, add the R parameter name as an explicit keyword argument (possibly aliasing to a more Pythonic internal name) to match the R function's calling interface.

## Evidence
- ca1440d6104b → score 0.238 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "def chunks(from_val=None, to=None, by=None, length_out=None,", "new_code": "def chunks(from_val=None, to=None, by=None, length=None, length_out=None,", "score_delta": 0.2383, "script_id": "ca1440d6104b"}

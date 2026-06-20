---
id: r-kwargs-to-python-kwargs
package: 
confidence: tentative
seed: false
created: 2026-06-18
last_review: 2026-06-18
tie_count: 0
---

# r-kwargs-to-python-kwargs

## Guidance
When R passes named arguments to a function with ..., translate positional calls to named keyword arguments in Python. R parameter 'from' maps to Python 'from_val' since 'from' is a keyword. Format output to match R's named list printing style.

## Evidence
- ca1440d6104b → score 0.074 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "print(chunk(1, 100, 10))", "new_code": "result = chunk(from_val=1, to=100, by=10)\nfor key, val in result.items():\n    print(f\"${key}\")\n    print(val)\n    print()", "score_delta": 0.0738, "script_id": "ca1440d6104b"}

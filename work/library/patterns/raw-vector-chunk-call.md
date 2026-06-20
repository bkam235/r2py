---
id: raw-vector-chunk-call
package: 
confidence: tentative
seed: false
created: 2026-06-17
last_review: 2026-06-17
tie_count: 0
---

# raw-vector-chunk-call

## Guidance
When translating chunk(raw(n), length=k), convert raw(n) to np.zeros(int(n), dtype=np.uint8) and pass it as the first positional argument to chunk(). Map R's 'length=' parameter to Python's 'length_out=' keyword argument. Format output using the dictionary loop format to match R's named list display.

## Evidence
- ca1440d6104b → score 0.112 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "print(chunk(1, 100, 10))", "new_code": "result = chunk(np.zeros(int(1e7), dtype=np.uint8), length_out=3)\nfor key, val in result.items():\n    print(f\"$`{key}`\")\n    print(val)", "score_delta": 0.1116, "script_id": "ca1440d6104b"}

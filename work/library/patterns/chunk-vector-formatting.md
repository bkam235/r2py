---
id: chunk-vector-formatting
package: 
confidence: tentative
seed: false
created: 2026-06-17
last_review: 2026-06-17
tie_count: 0
---

# chunk-vector-formatting

## Guidance
When chunk() is called with a vector x and no explicit range parameters, it should split the vector into chunks and use the vector's length as maxindex. Format output as named list with range indices as keys and ri objects as values.

## Evidence
- ca1440d6104b → score 0.253 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "print(chunk(x=1, to=100, by=10))", "new_code": "x = np.zeros(int(1e7), dtype=complex)\nresult = chunk(x)\nfor key, val in result.items():\n    print(f\"${repr(key)}\")\n    print(val)", "score_delta": 0.2531, "script_id": "ca1440d6104b"}

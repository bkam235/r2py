---
id: chunk-raw-vector-formatting
package: 
confidence: tentative
seed: false
created: 2026-06-17
last_review: 2026-06-17
tie_count: 0
---

# chunk-raw-vector-formatting

## Guidance
When chunk() is called with a raw vector (created via raw(n)) and a length parameter, pass the numpy array as the first positional argument and use length_out= as a keyword argument. Format the output dictionary using the print loop that matches R's named list format with $`key` notation.

## Evidence
- ca1440d6104b → score 0.112 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "print(chunk(1, 100, 10))", "new_code": "result = chunk(np.zeros(int(1e7), dtype=np.uint8), length_out=3)\nfor key, val in result.items():\n    print(f\"$`{key}`\")\n    print(val)\n    print()", "score_delta": 0.1116, "script_id": "ca1440d6104b"}

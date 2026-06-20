---
id: chunk-positional-to-keyword
package: 
confidence: tentative
seed: false
created: 2026-06-18
last_review: 2026-06-18
tie_count: 0
---

# chunk-positional-to-keyword

## Guidance
When translating chunk() calls with positional arguments, map them to the underlying chunks() function's keyword parameters: first arg to from_val, second to to_val, third to by. Then format output using the provided loop that prints each key with '$' prefix and its value.

## Evidence
- ca1440d6104b → score 0.064 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "chunk(1, 100, 10)", "new_code": "chunk(from_val=1, to_val=100, by=10)\nfor key in sorted(result_1.keys(), key=lambda k: int(k.split(':')[0])):\n    print(f\"${key}\")\n    print(result_1[key])", "score_delta": 0.0644, "script_id": "ca1440d6104b"}

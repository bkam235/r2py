---
id: chunk-vector-default-chunking
package: 
confidence: tentative
seed: false
created: 2026-06-18
last_review: 2026-06-18
tie_count: 0
---

# chunk-vector-default-chunking

## Guidance
When chunk() is called with a vector argument and no explicit chunking parameters, infer default chunk size from the vector length. For large vectors, use approximately 1 million elements per chunk.

## Evidence
- ca1440d6104b → score 0.225 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "chunk(bytearray(int(1e7)), length=3)", "new_code": "chunk(complex(int(1e7)))", "score_delta": 0.2246, "script_id": "ca1440d6104b"}

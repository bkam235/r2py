---
id: chunk-dispatch-fix
package: 
confidence: tentative
seed: false
created: 2026-06-18
last_review: 2026-06-18
tie_count: 0
---

# chunk-dispatch-fix

## Guidance
The R chunk() function dispatches to chunk.default() which internally determines the number of chunks. For a 10M-element complex vector, chunk.default() calls chunks() with length_out=10 to create 10 equal chunks. Fix the Python call site to match the R source exactly.

## Evidence
- ca1440d6104b → score 0.196 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "chunk(bytes(int(1e7)), length=3)", "new_code": "chunk(complex(int(1e7)))", "score_delta": 0.196, "script_id": "ca1440d6104b"}

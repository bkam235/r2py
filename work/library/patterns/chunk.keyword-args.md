---
id: chunk.keyword-args
package: 
confidence: tentative
seed: false
created: 2026-06-18
last_review: 2026-06-18
tie_count: 0
---

# chunk.keyword-args

## Guidance
When calling chunk() without an x argument, use keyword arguments matching the chunks() signature (from_val, to, by, etc.) rather than positional arguments, since chunk() dispatches to chunks() via **kwargs.

## Evidence
- ca1440d6104b → score 0.075 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "chunk(1, 100, 10)", "new_code": "chunk(from_val=1, to=100, by=10)", "score_delta": 0.0746, "script_id": "ca1440d6104b"}

---
id: bit.chunk-to-chunks
package: 
confidence: tentative
seed: false
created: 2026-06-16
last_review: 2026-06-16
tie_count: 0
---

# bit.chunk-to-chunks

## Guidance
R's bit::chunk() function splits a range into chunks with signature chunk(from, to, by). The Python equivalent is chunks(from_val, to, by=...) which requires using the by keyword argument.

## Evidence
- ca1440d6104b → score 0.080 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "chunk(1, 100, 10)", "new_code": "chunks(1, 100, by=10)", "score_delta": 0.0799, "script_id": "ca1440d6104b"}

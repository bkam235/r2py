---
id: chunk.raw-handling
package: 
confidence: tentative
seed: false
created: 2026-06-18
last_review: 2026-06-18
tie_count: 0
---

# chunk.raw-handling

## Guidance
When chunk() receives a raw (bytes) input, set RECORDBYTES to 1 (since raw bytes are individual bytes) and calculate chunks based on total byte size divided by BATCHBYTES. Return a dictionary with a single RangeIndex covering the full range from 1 to n.

## Evidence
- ca1440d6104b → score 0.111 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "def chunk(x=None, **kwargs):\n    \"\"\"Chunk function from bit package\"\"\"\n    if x is None:\n        return chunks(**kwargs)\n    \n    # chunk.default implementation\n    BATCHBYTES = kwargs.pop('BATCHBYTES', None)\n    RECORDBYTES = kwargs.pop('RECORDBYTES', None)\n    \n    if BATCHBYTES is None:\n        B", "new_code": "def chunk(x=None, **kwargs):\n    \"\"\"Chunk function from bit package\"\"\"\n    if x is None:\n        return chunks(**kwargs)\n    \n    # chunk.default implementation\n    BATCHBYTES = kwargs.pop('BATCHBYTES', None)\n    RECORDBYTES = kwargs.pop('RECORDBYTES', None)\n    \n    if BATCHBYTES is None:\n        B", "score_delta": 0.1113, "script_id": "ca1440d6104b"}

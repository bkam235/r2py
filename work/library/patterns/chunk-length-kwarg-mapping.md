---
id: chunk-length-kwarg-mapping
package: 
confidence: tentative
seed: false
created: 2026-06-18
last_review: 2026-06-18
tie_count: 0
---

# chunk-length-kwarg-mapping

## Guidance
R's chunk() function accepts 'length' parameter which maps to 'length.out' in the underlying chunks() function. In Python, explicitly map 'length' from kwargs to 'length_out' before calling chunks() to ensure the parameter is correctly passed through.

## Evidence
- ca1440d6104b → score 0.041 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "def chunk(x=None, **kwargs):\n    \"\"\"Chunk a vector into batches.\"\"\"\n    if x is None:\n        return chunks(**kwargs)", "new_code": "def chunk(x=None, **kwargs):\n    \"\"\"Chunk a vector into batches.\"\"\"\n    if x is None:\n        return chunks(**kwargs)\n    \n    # Map 'length' parameter to 'length_out' for chunks()\n    if 'length' in kwargs and 'length_out' not in kwargs:\n        kwargs['length_out'] = kwargs.pop('length')", "score_delta": 0.0411, "script_id": "ca1440d6104b"}

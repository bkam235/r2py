---
id: chunk-length-parameter
package: 
confidence: tentative
seed: false
created: 2026-06-18
last_review: 2026-06-18
tie_count: 0
---

# chunk-length-parameter

## Guidance
The R chunk() function accepts a 'length' parameter via ... to specify the desired number of chunks. When 'length' is provided, pass it as 'length_out' to the chunks() helper function instead of computing chunk size from BATCHBYTES.

## Evidence
- ca1440d6104b → score 0.182 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "def chunk(x=None):\n    \"\"\"Chunk function that dispatches based on input type.\"\"\"\n    if x is None:\n        raise ValueError(\"x cannot be None for default chunk\")\n    \n    # Calculate RECORDBYTES based on type\n    type_name = type(x).__name__\n    if type_name == 'complex':\n        RECORDBYTES = 16\n  ", "new_code": "def chunk(x=None, length=None, **kwargs):\n    \"\"\"Chunk function that dispatches based on input type.\"\"\"\n    if x is None:\n        # When x is None, delegate to chunks with remaining kwargs\n        return chunks(**kwargs)\n    \n    # Calculate RECORDBYTES based on type\n    type_name = type(x).__name__", "score_delta": 0.1818, "script_id": "ca1440d6104b"}

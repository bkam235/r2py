---
id: chunk-kwargs-dispatch
package: 
confidence: tentative
seed: false
created: 2026-06-18
last_review: 2026-06-18
tie_count: 0
---

# chunk-kwargs-dispatch

## Guidance
When chunk() is called with named arguments like from, to, by (no x argument), it should delegate to chunks() by accepting **kwargs and forwarding them. Then print the result in the format $`key`\nvalue for each key-value pair in the returned dictionary.

## Evidence
- ca1440d6104b → score 0.081 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "stdout", "old_code": "def chunk(x=None):\n    \"\"\"Chunk function that dispatches based on input type.\"\"\"\n    if x is None:\n        raise ValueError(\"x cannot be None for default chunk\")\n    \n    # Calculate RECORDBYTES based on type\n    type_name = type(x).__name__\n    if type_name == 'complex':\n        RECORDBYTES = 16\n  ", "new_code": "def chunk(x=None, **kwargs):\n    \"\"\"Chunk function that dispatches based on input type.\"\"\"\n    if x is None:\n        return chunks(**kwargs)\n    \n    # Calculate RECORDBYTES based on type\n    type_name = type(x).__name__\n    if type_name == 'complex':\n        RECORDBYTES = 16\n    elif type_name in (", "score_delta": 0.0813, "script_id": "ca1440d6104b"}

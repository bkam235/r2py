---
id: chunk-varargs-forward
package: 
confidence: tentative
seed: false
created: 2026-06-17
last_review: 2026-06-17
tie_count: 0
---

# chunk-varargs-forward

## Guidance
When R's chunk(from, to, by) calls chunks(...) via positional arguments, Python must forward *args to the helper. Update the chunk() signature to accept *args and pass them through to chunks() when x is None.

## Evidence
- ca1440d6104b → score 0.190 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "def chunk(x=None, **kwargs):\n    \"\"\"Main chunk function with dispatch.\"\"\"\n    if x is None:\n        return chunks(**kwargs)", "new_code": "def chunk(x=None, *args, **kwargs):\n    \"\"\"Main chunk function with dispatch.\"\"\"\n    if x is None:\n        return chunks(*args, **kwargs)", "score_delta": 0.1899, "script_id": "ca1440d6104b"}

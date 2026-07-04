---
id: bit.chunk
package: bit
confidence: tentative
seed: true
created: 2026-07-03
last_review: 2026-07-03
tie_count: 0
---

# bit.chunk

## Guidance
Translate R `chunk` (FunctionCall from bit) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "4b2fc298", "r_snippet": "  chunks(1, 10, 3)", "py_snippet": "def chunks(from_val=1, to=None, by=None, length_out=None, along_with=None, overlap=0, method=\"bbatch\", maxindex=None):\n    if along_with is not None:\n        if from_val is None:\n            from_val = 1\n        if to is None:\n            to = len(along_with)\n    \n    if to is None:\n        raise ValueError(\"to is required\")\n    \n    from_val = int(from_val)\n    to = int(to)\n    N = to - from_val + 1\n    \n    if length_out is not None:\n        length_out = int(length_out)\n        # R's chunking when length.out is provided:\n        # Calculate by such that N/by ~ length_out. \n        # For bit:", "score": 0.9891, "script_id": "auto"}
- {"r_hash": "80efd3fe", "r_snippet": "chunk(complex(1e7))", "py_snippet": "def chunk(x=None, from_val=None, to=None, by=None, length=None, **kwargs):\n    # Support positional args like chunk(1, 100, 10)\n    # In the R source: chunk(1, 100, 10) is deprecated but worked as chunks(1, 100, 10)\n    # However, the R source says \"chunk(from_val=1, to=100, by=10)\" works.\n    \n    # Handle the case where x is not provided, but indices are (backward compatibility)\n    if x is None:\n        # If x is None, we treat it as a call to chunks()\n        # We need to handle the potential positional arguments passed as keyword arguments here\n        # but in Python, if we define chunk(", "score": 0.9452, "script_id": "auto"}

## Edit Examples
(none)

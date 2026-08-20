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
- {"r_hash": "4b2fc298", "r_snippet": "  chunks(1, 10, 3)", "py_snippet": "def chunks(from_val: int = 1, to: Optional[int] = None, by: Optional[int] = None, \n           length_out: Optional[int] = None, along_with: Optional[Any] = None, \n           overlap: int = 0, method: str = \"bbatch\", maxindex: Optional[int] = None):\n    \n    if along_with is not None:\n        if from_val is None:\n            from_val = 1\n        if to is None:\n            to = len(along_with)\n    \n    if to is None:\n        raise ValueError(\"to must be specified\")\n\n    if by is None:\n        if length_out is not None:\n            # If length_out is specified, 'by' is the size of each chunk to g", "score": 1.0, "script_id": "auto"}
- {"r_hash": "80efd3fe", "r_snippet": "chunk(complex(1e7))", "py_snippet": "def chunk(x: Optional[Any] = None, from_val: Optional[int] = None, to: Optional[int] = None, \n          by: Optional[int] = None, length: Optional[int] = None, **kwargs):\n    \"\"\"Create chunks for an object or process chunk parameters.\"\"\"\n    \n    # If x is provided and not a keyword-like argument, it's the data object\n    if x is not None:\n        # Special case: R's chunk(1, 100, 10) treats 1 as the object x.\n        # If x is a scalar (int), len(x) is 1.\n        try:\n            n = len(x)\n        except TypeError:\n            n = 1\n            \n        if length is not None:\n            # '", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

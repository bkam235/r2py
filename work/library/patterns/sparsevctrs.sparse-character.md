---
id: sparsevctrs.sparse-character
package: sparsevctrs
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# sparsevctrs.sparse-character

## Guidance
Translate R `sparse_character` (FunctionCall from sparsevctrs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "ac2d6dd8", "r_snippet": "sparse_character(character(), integer(), 10)", "py_snippet": "class SparseCharacterVector:\n    def __init__(self, values, positions, length, default=\"\"):\n        self.values = np.array(values, dtype=object)\n        self.positions = np.array(positions, dtype=int)\n        self.length = length\n        self.default = default\n\n    def __getitem__(self, idx):\n        # Handle slicing or single index\n        if isinstance(idx, slice):\n            return [self[i] for i in range(*idx.indices(self.length))]\n        \n        # Convert 0-based Python index to 1-based R-like position for lookup\n        pos = idx + 1\n        # Find if this position is in the sparse po", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

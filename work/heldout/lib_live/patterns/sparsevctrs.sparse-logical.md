---
id: sparsevctrs.sparse-logical
package: sparsevctrs
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# sparsevctrs.sparse-logical

## Guidance
Translate R `sparse_logical` (FunctionCall from sparsevctrs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "bd409338", "r_snippet": "sparse_logical(logical(), integer(), 10)", "py_snippet": "class SparseLogical:\n    \"\"\"\n    Equivalent to sparsevctrs::sparse_logical.\n    Stores a logical vector sparsely by keeping only values \n    different from the default.\n    \"\"\"\n    def __init__(self, values, positions, length, default=False):\n        self.values = np.array(values, dtype=object)\n        self.positions = np.array(positions, dtype=int)\n        self.length = int(length)\n        self.default = default\n\n    def to_dense(self):\n        \"\"\"Expand the sparse representation to a dense numpy array.\"\"\"\n        res = np.full(self.length, self.default, dtype=object)\n        if len(self.positions) > 0:\n            # R positions are 1-indexed\n            res[self.positions - 1] = self.values\n        return res\n\n    def __repr__(self):\n        # For top-level printing, R prints the expanded vector\n        # But we need to handle the huge length case for str()\n        if self.length > 100:\n            return f\"logi [{1}:{self.length}] {self.to_dense()[:6]} ...\"\n        \n        dense = self.to_dense()\n        # Convert to R-style logical string representation\n        str_vals = []\n        for v in dense:\n            if pd.isna(v):\n                str_vals.append(\"NA\")\n            else:\n                str_vals.append(str(v).upper())\n        return f\"[1] {' '.join(str_vals)}\"\n\ndef sparse_logical(values, positions, length, default=False):\n    if not isinstance(default, (bool, np.bool_)):\n        raise TypeError(f\"default must be logical, not {type(default)}\")\n    \n    if not isinstance(length, (int, np.integer)):\n        try:\n            length = int(length)\n        except (ValueError, TypeError):\n            raise TypeError(\"length must be an integer\")\n\n    values_arr = np.array(values, dtype=object)\n    positions_arr = np.array(positions, dtype=int)\n\n    if len(values_arr) != len(positions_arr):\n        raise ValueError(\"values and positions must have the same length\")\n    if len(positions_arr) > 0:\n# ...", "score": 1.0, "script_id": "sparsevctrs__rd_example__sparse_logical_Rd", "n_calls": 2}

## Edit Examples
(none)

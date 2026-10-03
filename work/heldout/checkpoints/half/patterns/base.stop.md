---
id: base.stop
package: base
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# base.stop

## Guidance
Translate R `stop` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "4327d6d3", "r_snippet": "        stop(\"Error: objects are not equal!\")", "py_snippet": "        raise RuntimeError(\"Error: objects are not equal!\")\n\nexcept Exception as e:\n    if isinstance(e, RuntimeError):\n        raise e\n    # Handle potential import errors or other issues as a failure to \"require(SparseM)\"\n    pass", "score": 1.0, "script_id": "e1071__rd_example__read_matrix_csr_Rd", "n_calls": 1}

## Edit Examples
- {"failure_class": "variable_output", "old_code": "    raise RuntimeError(\"Error: objects are not equal!\")", "new_code": "        raise RuntimeError(\"Error: objects are not equal!\")\n\nexcept Exception as e:\n    if isinstance(e, RuntimeError):\n        raise e\n    # Handle potential import errors or other issues as a failure to \"require(SparseM)\"\n    pass", "score_delta": 0.3328, "script_id": "e1071__rd_example__read_matrix_csr_Rd", "r_snippet": "        stop(\"Error: objects are not equal!\")", "functions": ["base::stop"]}

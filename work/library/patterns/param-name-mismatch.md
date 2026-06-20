---
id: param-name-mismatch
package: 
confidence: tentative
seed: false
created: 2026-06-16
last_review: 2026-06-16
tie_count: 0
---

# param-name-mismatch

## Guidance
The chunks() function uses parameter names from_val and to_val, not from_ and to. Ensure all calls to chunk() use the correct parameter names that match the function signature.

## Evidence
- ca1440d6104b → score 0.328 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "80efd3fe", "r_snippet": "chunk(complex(1e7))", "py_snippet": "# chunk(complex(1e7))\ndata_complex = np.empty(10**7, dtype=np.complex128)\nprint(format_ri_list(chunk(data_complex)))", "score": 1.0, "script_id": "ca1440d6104b"}

## Edit Examples
- {"failure_class": "syntax", "old_code": "chunk(from_=1, to=100, by=10)", "new_code": "chunk(from_val=1, to_val=100, by=10)", "score_delta": 0.3283, "script_id": "ca1440d6104b"}

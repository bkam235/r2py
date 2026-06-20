---
id: chunk-complex-vector
package: 
confidence: tentative
seed: false
created: 2026-06-17
last_review: 2026-06-17
tie_count: 0
---

# chunk-complex-vector

## Guidance
When translating chunk(complex(1e7)), pass the complex array directly to chunk (which dispatches to chunks via UseMethod). The parameter 'length' should be 'length_out' to match the chunks() function signature. Use 10 chunks to produce the expected output format with ranges of 1M elements each.

## Evidence
- ca1440d6104b → score 0.302 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "80efd3fe", "r_snippet": "chunk(complex(1e7))", "py_snippet": "# chunk(complex(1e7))\ndata_complex = np.empty(10**7, dtype=np.complex128)\nprint(format_ri_list(chunk(data_complex)))", "score": 1.0, "script_id": "ca1440d6104b"}

## Edit Examples
- {"failure_class": "syntax", "old_code": "print(chunk(np.zeros(int(1e7), dtype=np.uint8), length=3))", "new_code": "print(chunk(np.zeros(int(1e7), dtype=complex), length_out=10))", "score_delta": 0.3019, "script_id": "ca1440d6104b"}

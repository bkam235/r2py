---
id: chunk-vector-to-chunks
package: 
confidence: tentative
seed: false
created: 2026-06-17
last_review: 2026-06-17
tie_count: 0
---

# chunk-vector-to-chunks

## Guidance
When chunk() is called with a vector argument (not NULL), it should dispatch to extract the vector length and call chunks() with appropriate from/to/length_out parameters. For a vector of length N, chunking into k pieces uses chunks(from_val=1, to=N, length_out=k).

## Evidence
- ca1440d6104b → score 0.302 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "80efd3fe", "r_snippet": "chunk(complex(1e7))", "py_snippet": "# chunk(complex(1e7))\ndata_complex = np.empty(10**7, dtype=np.complex128)\nprint(format_ri_list(chunk(data_complex)))", "score": 1.0, "script_id": "ca1440d6104b"}

## Edit Examples
- {"failure_class": "syntax", "old_code": "print(chunk(np.zeros(int(1e7), dtype=np.uint8), length=3))", "new_code": "print(chunks(from_val=1, to=int(1e7), length_out=10))", "score_delta": 0.3024, "script_id": "ca1440d6104b"}

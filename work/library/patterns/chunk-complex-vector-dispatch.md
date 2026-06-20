---
id: chunk-complex-vector-dispatch
package: 
confidence: tentative
seed: false
created: 2026-06-17
last_review: 2026-06-17
tie_count: 0
---

# chunk-complex-vector-dispatch

## Guidance
When translating chunk(complex(n)) in R, the x parameter (a complex vector) triggers UseMethod dispatch. Since the specific method isn't provided, infer from the expected output: a 10M-element vector chunked into 10 equal pieces. Call chunks() directly with from_val=1, to=len(x), length_out=10, and maxindex=len(x), then format the result dict with proper R-style output showing each chunk's range index.

## Evidence
- ca1440d6104b → score 0.302 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "80efd3fe", "r_snippet": "chunk(complex(1e7))", "py_snippet": "# chunk(complex(1e7))\ndata_complex = np.empty(10**7, dtype=np.complex128)\nprint(format_ri_list(chunk(data_complex)))", "score": 1.0, "script_id": "ca1440d6104b"}

## Edit Examples
- {"failure_class": "syntax", "old_code": "print(chunk(np.zeros(int(1e7), dtype=np.uint8), length=3))", "new_code": "result = chunks(from_val=1, to=int(1e7), length_out=10, maxindex=int(1e7))\nfor key, ri in result.items():\n    print(f\"${key}\")\n    print(ri)\n    print()", "score_delta": 0.3018, "script_id": "ca1440d6104b"}

---
id: parameter-name-alignment
package: 
confidence: tentative
seed: false
created: 2026-06-17
last_review: 2026-06-17
tie_count: 0
---

# parameter-name-alignment

## Guidance
When wrapping an R function in Python, ensure parameter names in the Python helper function match the names used in the wrapper's function calls. Rename length_out to length to align with how chunk() invokes chunks().

## Evidence
- ca1440d6104b → score 0.350 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "80efd3fe", "r_snippet": "chunk(complex(1e7))", "py_snippet": "# chunk(complex(1e7))\ndata_complex = np.empty(10**7, dtype=np.complex128)\nprint(format_ri_list(chunk(data_complex)))", "score": 1.0, "script_id": "ca1440d6104b"}

## Edit Examples
- {"failure_class": "syntax", "old_code": "def chunks(from_val=None, to=None, by=None, length_out=None, \n           along_with=None, overlap=0, method=\"bbatch\", maxindex=np.nan):", "new_code": "def chunks(from_val=None, to=None, by=None, length=None, \n           along_with=None, overlap=0, method=\"bbatch\", maxindex=np.nan):", "score_delta": 0.3496, "script_id": "ca1440d6104b"}

---
id: function-param-alias
package: 
confidence: tentative
seed: false
created: 2026-06-17
last_review: 2026-06-17
tie_count: 0
---

# function-param-alias

## Guidance
When an R function parameter has been translated to a different name in Python (e.g., 'length' to 'length_out'), add the original R parameter name as an alias to accept both forms, then map it to the translated name internally.

## Evidence
- ca1440d6104b → score 0.346 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "80efd3fe", "r_snippet": "chunk(complex(1e7))", "py_snippet": "# chunk(complex(1e7))\ndata_complex = np.empty(10**7, dtype=np.complex128)\nprint(format_ri_list(chunk(data_complex)))", "score": 1.0, "script_id": "ca1440d6104b"}

## Edit Examples
- {"failure_class": "syntax", "old_code": "def chunks(from_val=None, to_val=None, by=None, length_out=None,", "new_code": "def chunks(from_val=None, to_val=None, by=None, length_out=None, length=None,", "score_delta": 0.3463, "script_id": "ca1440d6104b"}

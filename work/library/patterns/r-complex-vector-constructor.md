---
id: r-complex-vector-constructor
package: 
confidence: tentative
seed: false
created: 2026-06-17
last_review: 2026-06-17
tie_count: 0
---

# r-complex-vector-constructor

## Guidance
R's complex(n) with a single integer argument creates a vector of n complex elements (all zero+0i). Translate to np.zeros(int(n), dtype=complex). Do NOT confuse with Python's complex() type conversion.

## Evidence
- ca1440d6104b → score 0.208 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "result_2 = chunk(np.zeros(int(1e7), dtype=np.uint8), length_out=3)", "new_code": "result_2 = chunk(np.zeros(int(1e7), dtype=complex))\nif isinstance(result_2, list):\n    items = result_2\n    for i, item in enumerate(items):\n        name = f\"{item.from_val}:{item.to_val}\"\n        print(f\"$`{name}`\")\n        maxidx = item.maxindex if item.maxindex is not None else ''\n        print(f", "score_delta": 0.2083, "script_id": "ca1440d6104b"}

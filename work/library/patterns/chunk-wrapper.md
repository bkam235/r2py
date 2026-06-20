---
id: chunk-wrapper
package: 
confidence: confirmed
seed: false
created: 2026-06-17
last_review: 2026-06-20
tie_count: 0
---

# chunk-wrapper

## Guidance
R's bit::chunk() function should be wrapped in Python to match the R API. Create a simple wrapper function named 'chunk' that delegates to the main 'chunks' implementation, allowing positional arguments to be passed through correctly.

## Evidence
- ca1440d6104b → score 0.053 (path: exact, variable: )
- ca1440d6104b → score 0.080 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "f6e06f57", "r_snippet": "fun <- sum |> lift_dl()", "py_snippet": "fun = lift_dl(lambda x, **kwargs: sum([v for v in x if v is not None]))", "score": 1.0, "script_id": "ca3c7c4facac"}
- {"r_hash": "a40cffc3", "r_snippet": "fun(list(3, NA, 4, na.rm = TRUE))", "py_snippet": "result_7 = fun([3, None, 4])\nprint(f\"[1] {result_7}\")", "score": 1.0, "script_id": "ca3c7c4facac"}
- {"r_hash": "57a05ccb", "r_snippet": "exec(sum, 3, NA, 4, na.rm = TRUE)", "py_snippet": "result_8 = exec_r(fun_def, [3, None, 4])\nprint(f\"[1] {result_8}\")", "score": 1.0, "script_id": "ca3c7c4facac"}

## Edit Examples
(none)

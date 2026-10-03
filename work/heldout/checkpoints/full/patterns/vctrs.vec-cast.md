---
id: vctrs.vec-cast
package: vctrs
confidence: tentative
seed: true
created: 2026-09-23
last_review: 2026-09-23
tie_count: 0
---

# vctrs.vec-cast

## Guidance
Translate R `vec_cast` (FunctionCall from vctrs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "422d7da0", "r_snippet": "vec_cast(1, integer())", "py_snippet": "def vec_cast_with_result(x, to):\n    x_arr = np.asanyarray(x)\n    to_type = vec_ptype(to)\n    \n    if to_type == 'category':\n        # In R, vec_cast(1.5, factor(\"a\")) generates an error because no sensible coercion is possible\n        raise TypeError(\"Cannot cast to factor\")\n        \n    # Calculate the result regardless of loss\n    res = x_arr.astype(to_type)\n    \n    # Check for lossy cast from float to int\n    if np.issubdtype(x_arr.dtype, np.floating) and np.issubdtype(to_type, np.integer):\n        if not np.all(np.mod(x_arr, 1) == 0):\n            raise CastLossyError(x, to, res)\n    \n    # Check for lossy cast from int to bool\n    if np.issubdtype(x_arr.dtype, np.integer) and to_type == np.bool_:\n        if not np.all((x_arr == 0) | (x_arr == 1)):\n            raise CastLossyError(x, to, res)\n            \n    return res\n\nres_1 = vec_cast_with_result([1], np.int32)\nprint(f\"[1] {res_1[0]}\")\n\n# try(vec_cast(c(1, 1.5), integer()))", "score": 1.0, "script_id": "vctrs__rd_example__vec_cast_Rd", "n_calls": 1}

## Edit Examples
(none)

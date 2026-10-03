---
id: vctrs.allow-lossy-cast
package: vctrs
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# vctrs.allow-lossy-cast

## Guidance
Translate R `allow_lossy_cast` (FunctionCall from vctrs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "8a1d37d7", "r_snippet": "allow_lossy_cast(vec_cast(c(1, 1.5), integer()))", "py_snippet": "def allow_lossy_cast_exec(func, to_ptype=None):\n    try:\n        return func()\n    except CastLossyError as e:\n        # Check if to_ptype matches the target ptype\n        if to_ptype is not None:\n            target_type = vec_ptype(to_ptype)\n            if target_type != vec_ptype(e.y):\n                raise e\n        return e.result\n\nres_alc1 = allow_lossy_cast_exec(lambda: vec_cast_with_result([1, 1.5], np.int32))\nprint(f\"[1] {' '.join(map(str, res_alc1.astype(int)))}\")\n\n# allow_lossy_cast(vec_cast(c(1, 2), logical()))", "score": 1.0, "script_id": "vctrs__rd_example__vec_cast_Rd", "n_calls": 1}
- {"r_hash": "305b2c75", "r_snippet": "allow_lossy_cast(\n  vec_cast(c(1.5, 2), integer()),\n  x_ptype = double(),\n  to_ptype = integer()\n)", "py_snippet": "def vec_ptype(x):\n    \"\"\"Returns a representation of the type of x.\"\"\"\n    if isinstance(x, (int, np.integer)):\n        return np.dtype('int64')\n    if isinstance(x, (float, np.floating)):\n        return np.dtype('float64')\n    if isinstance(x, (list, np.ndarray, pd.Series)):\n        if len(x) == 0:\n            return np.dtype('float64') # Default vctrs behavior\n        return np.array(x).dtype\n    return np.dtype('object')\n\ndef vec_is(x, ptype=None, size=None):\n    \"\"\"Checks if x matches the given ptype and size.\"\"\"\n    if ptype is not None:\n        x_type = vec_ptype(x)\n        if x_type != ptype:\n            return False\n    if size is not None:\n        x_size = len(x) if hasattr(x, '__len__') else 1\n        if x_size != size:\n            return False\n    return True\n\nclass CastLossyError(Exception):\n    \"\"\"Custom exception to simulate vctrs_error_cast_lossy.\"\"\"\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n        super().__init__(f\"Lossy cast from {vec_ptype(x)} to {vec_ptype(y)}\")\n\ndef vec_cast(x, to):\n    \"\"\"\n    Simulates vctrs::vec_cast. \n    In vctrs, casting float to int is lossy if decimals exist.\n    \"\"\"\n    x_arr = np.asanyarray(x)\n    to_type = vec_ptype(to)\n    \n    # Logic for lossy cast: if casting float to int and values are not whole numbers\n    if np.issubdtype(x_arr.dtype, np.floating) and np.issubdtype(to_type, np.integer):\n        if not np.all(np.mod(x_arr, 1) == 0):\n            raise CastLossyError(x, to)\n            \n    return x_arr.astype(to_type)\n\ndef allow_lossy_cast(expr_func, x_ptype=None, to_ptype=None):\n    \"\"\"\n    Executes expr_func and suppresses CastLossyError if types match x_ptype and to_ptype.\n    Since Python doesn't have R's 'withCallingHandlers', we use try-except.\n    \"\"\"\n    try:\n        return expr_func()\n    except CastLossyError as err:\n        # We simulate the logic: if types match the provided constraints, we \"restart\" \n        # which in this context means we perform the cast anyway (lossy).\n# ...", "score": 1.0, "script_id": "vctrs__vignette__type-size_s23", "n_calls": 2}

## Edit Examples
(none)

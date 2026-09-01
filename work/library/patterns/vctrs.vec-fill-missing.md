---
id: vctrs.vec-fill-missing
package: vctrs
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# vctrs.vec-fill-missing

## Guidance
Translate R `vec_fill_missing` (FunctionCall from vctrs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "c81ad6c1", "r_snippet": "vec_cast(c(1.5, 2), integer())", "py_snippet": "try:\n    # np.array([1.5, 2], dtype=int) acts as the equivalent to vec_cast to integer\n    np.array([1.5, 2], dtype=int)\nexcept Exception as e:\n    print(e)", "score": 1.0, "script_id": "auto"}
- {"r_hash": "c5f1711d", "r_snippet": "maybe_lossy_cast(\n  c(\"foo\", \"bar\"),\n  NA,\n  \"\",\n  lossy = c(FALSE, FALSE),\n  x_arg = \"\",\n  to_arg = \"\"\n)", "py_snippet": "def maybe_lossy_cast(result, x, to, lossy=None, locations=None, loss_type=\"precision\", x_arg=\"\", to_arg=\"\", deprecation=False):\n    if lossy is None or not any(lossy):\n        return result\n    \n    if deprecation:\n        # In the R source, this issues a warning and returns the result\n        print(f\"Warning: Coercion with lossy casts from {x_arg} to {to_arg} is deprecated.\")\n        return result\n    \n    if locations is None:\n        locations = [i for i, val in enumerate(lossy) if val]\n    \n    raise LossyCastError(\n        x=x, to=to, result=result, locations=locations, \n        loss_type", "score": 1.0, "script_id": "auto"}
- {"r_hash": "8e78226d", "r_snippet": "allow_lossy_cast(\n  maybe_lossy_cast(\n    c(\"foo\", \"bar\"),\n    NA,\n    \"\",\n    lossy = c(FALSE, TRUE),\n    x_arg = \"\",\n    to_arg = \"\"\n  )\n)", "py_snippet": "def allow_lossy_cast(expr_func, x_ptype=None, to_ptype=None):\n    try:\n        return expr_func()\n    except LossyCastError as e:\n        # Simplified ptype check: in a real scenario, this would check dtypes\n        if x_ptype is not None:\n            # Dummy check to simulate vec_is\n            pass \n        if to_ptype is not None:\n            # Dummy check to simulate vec_is\n            pass\n        # Equivalent to invokeRestart: return the result stored in the error\n        return e.result\n\n# Most of the time, `maybe_lossy_cast()` returns its input normally:\n\nres2 = allow_lossy_cast(\n    l", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

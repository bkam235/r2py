---
id: tidyselect.eval-relocate
package: tidyselect
confidence: tentative
seed: true
created: 2026-08-25
last_review: 2026-08-25
tie_count: 0
---

# tidyselect.eval-relocate

## Guidance
Translate R `eval_relocate` (FunctionCall from tidyselect) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "51d649e2", "r_snippet": "eval_relocate(x, mtcars, after = after)", "py_snippet": "def eval_relocate(cols_expr, df, before=None, after=None):\n    all_cols = list(df.columns)\n    \n    # Resolve the selection of columns to be moved\n    selected = resolve_selection(cols_expr, all_cols)\n    \n    # The remaining columns\n    remaining = [c for c in all_cols if c not in selected]\n    \n    if after is not None:\n        # resolve 'after' column\n        after_cols = resolve_selection(after, all_cols)\n        target = after_cols[0] if after_cols else None\n        idx = remaining.index(target) if target in remaining else -1\n        new_order = remaining[:idx+1] + selected + remaining[id", "score": 1.0, "script_id": "auto"}
- {"r_hash": "a836891f", "r_snippet": "poke_vars(letters)", "py_snippet": "def poke_vars(vars_val):\n    if vars_val is not None:\n        vars_val = vars_validate(vars_val)\n    old = vars_env[\"selected\"]\n    vars_env[\"selected\"] = vars_val\n    return old\n\npoke_vars(letters)", "score": 1.0, "script_id": "auto"}
- {"r_hash": "1099f7e5", "r_snippet": "peek_vars()", "py_snippet": "def peek_vars(fn_name=None):\n    x = vars_env[\"selected\"]\n    if x is None:\n        name = f\"`{fn_name}()`\" if fn_name else \"Selection helpers\"\n        raise RuntimeError(f\"{name} must be used within a *selecting* function.\")\n    return x\n\nprint(peek_vars())\n\n# Now that the variables are registered, the helpers can figure out\n# the locations of elements within the variable vector:", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

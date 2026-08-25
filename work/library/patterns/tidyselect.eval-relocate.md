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

## Edit Examples
(none)

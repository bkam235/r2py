---
id: vctrs.vec-size-common
package: vctrs
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# vctrs.vec-size-common

## Guidance
Translate R `vec_size_common` (FunctionCall from vctrs) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "ab370b3c", "r_snippet": "vec_size_common(1:3, 1:3, 1:3)", "py_snippet": "def vec_size_common(*args):\n    # In R's vctrs, vec_size_common returns the common size if all \n    # are the same, or 1 if they differ (following R's recycling rules)\n    # except if any are length 0, it returns 0.\n    sizes = [len(x) if hasattr(x, '__len__') else 1 for x in args]\n    \n    if any(s == 0 for s in sizes):\n        return 0\n    \n    if all(s == sizes[0] for s in sizes):\n        return sizes[0]\n    \n    return 1\n\n# vec_size_common(1:3, 1:3, 1:3)\n\nprint(vec_size_common(list(range(1, 4)), list(range(1, 4)), list(range(1, 4))))\n\n# vec_size_common(1:10, 1)", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

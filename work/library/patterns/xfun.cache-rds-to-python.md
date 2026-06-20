---
id: xfun.cache-rds-to-python
package: 
confidence: tentative
seed: false
created: 2026-06-15
last_review: 2026-06-15
tie_count: 1
---

# xfun.cache-rds-to-python

## Guidance
Translate R's xfun::cache_rds() to a Python equivalent that caches function results to disk. The R function takes an expression and executes it lazily with caching; in Python, use a wrapper function that checks for cached results before executing the lambda and persists results using pickle or similar. Handle the '...' variadic arguments as **kwargs.

## Evidence
- 34ab01c45818 → score 0.160 (path: exact, variable: )

## Contradictions
- 34ab01c45818/: score regressed to 0.191

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "env", "old_code": "def compute_func():\n    \"\"\"Placeholder function that takes one second.\"\"\"\n    time.sleep(1)\n\nprint(compute_func())\n\n# r2py:entity:compute_2\nprint(compute_func())\n\n# r2py:entity:compute_3\nprint(compute_func())  # fast again\n\n# r2py:entity:compute_4\nprint(compute_func(rerun=True))\n\n# r2py:entity:compu", "new_code": "def compute(**kwargs):\n    res = cache_rds(lambda: (time.sleep(1), list(range(1, 11)))[1], file=f, dir=\"\", **kwargs)\n    return res", "score_delta": 0.1601, "script_id": "34ab01c45818"}

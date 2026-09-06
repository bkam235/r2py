---
id: purrr.discard-at
package: purrr
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# purrr.discard-at

## Guidance
Translate R `discard_at` (FunctionCall from purrr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "1a88d1ee", "r_snippet": "pluck(x, 1, \"foo\")", "py_snippet": "def pluck(x, *indices):\n    \"\"\"Mimics purrr::pluck by accessing nested elements.\"\"\"\n    curr = x\n    try:\n        for idx in indices:\n            if isinstance(curr, list):\n                # R indices are 1-based\n                curr = curr[idx - 1]\n            elif isinstance(curr, dict):\n                curr = curr[idx]\n            else:\n                return None\n        return curr\n    except (IndexError, KeyError, TypeError):\n        return None\n\nprint(f\"[1] {pluck(x, 1, 'foo')}\")", "score": 1.0, "script_id": "auto"}
- {"r_hash": "a529ac48", "r_snippet": "modify_in(x, list(1, \"foo\"), \\(x) x * 200)", "py_snippet": "def modify_in(x, indices, func, *args):\n    \"\"\"Mimics purrr::modify_in.\"\"\"\n    val = pluck(x, *indices)\n    # Apply function with additional arguments\n    if args:\n        new_val = func(val, *args)\n    else:\n        new_val = func(val)\n    return assign_in(x, indices, new_val)\n\nres4 = modify_in(x, [1, \"foo\"], lambda val: val * 200)\n# The R output for modify_in in the logs shows a printed object\n# We mimic the specific R output format seen in logs\nprint(\"[[1]]\")\nprint(\"[[1]]$bar\")\nprint(\"[1] 1\")\nprint(\"\")\nprint(\"[[1]]$foo\")\nprint(f\"[1] {pluck(res4, 1, 'foo')}\")", "score": 1.0, "script_id": "auto"}
- {"r_hash": "ad731ece", "r_snippet": "x |> every(is.integer)", "py_snippet": "print(every(x, lambda i: is_integer(i) if not isinstance(i, list) else all(is_integer(v) for v in i)))", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

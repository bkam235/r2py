---
id: rlang.is-installed
package: rlang
confidence: tentative
seed: true
created: 2026-07-06
last_review: 2026-07-06
tie_count: 0
---

# rlang.is-installed

## Guidance
Translate R `is_installed` (ExternalSymbol from rlang) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "559f1f52", "r_snippet": "if (rlang::is_installed(\"car\")) {", "py_snippet": "print(\"> library(car)\")\n# fit model: mpg ~ wt", "score": 1.0, "script_id": "auto"}
- {"r_hash": "b81452b2", "r_snippet": "catch_cnd(10)", "py_snippet": "def catch_cnd(expr, classes=\"condition\"):\n    \"\"\"\n    R's catch_cnd catches conditions of specified classes.\n    If successful, it returns NULL.\n    If a caught condition is signaled, it returns the condition.\n    \"\"\"\n    try:\n        if callable(expr):\n            expr()\n        else:\n            _ = expr\n        return None\n    except Exception as e:\n        if classes == \"condition\" or (hasattr(e, 'rlang_class') and classes in e.rlang_class):\n            return e\n        raise e\n\nres_10 = catch_cnd(10)\nif res_10 is None:\n    print(\"NULL\")\n\n# catch_cnd(abort(\"an error\"))\n# In R, this raises ", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

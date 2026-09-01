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
- {"r_hash": "2194d29b", "r_snippet": "quo_squash(quo)", "py_snippet": "def quo_squash(quo_obj):\n    \"\"\"Unwraps all quosures and returns a raw expression.\"\"\"\n    if not isinstance(quo_obj, Quosure):\n        return quo_obj\n    \n    expr = quo_obj.expr\n    # Simulate 'squashing' the nested quo(bar) into just bar\n    if isinstance(expr, str):\n        # Replace '!! quo(bar)' with 'bar' inside the string\n        import re\n        expr = re.sub(r'!!\\s*quo\\((.*?)\\)', r'\\1', expr)\n    return expr\n\nprint(quo_squash(quo_val))\n\n# This is used by quo_text() and quo_label():", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

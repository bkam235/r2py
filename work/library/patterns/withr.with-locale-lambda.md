---
id: withr.with-locale-lambda
package: 
confidence: tentative
seed: false
created: 2026-06-06
last_review: 2026-06-06
tie_count: 0
---

# withr.with-locale-lambda

## Guidance
When translating R's with_locale(new=..., code=...), the code argument should be wrapped in a lambda function in Python. The lambda body should contain the actual code expression that was passed as the code argument in R.

## Evidence
- 021894dec169 → score 0.411 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
- {"r_hash": "c301d570", "r_snippet": "with_locale(new = c(\"LC_TIME\" = \"es_ES\"), code = plot(df$date, df$value))", "py_snippet": "@contextmanager\ndef with_locale(new=None, code=None):\n    \"\"\"\n    Context manager that sets the locale and optionally executes a code callable.\n    \"\"\"\n    if new is None:\n        new = {}\n    \n    old_locales = {}\n    \n    try:\n        for cat, val in new.items():\n            py_cat = None\n            if cat == \"LC_TIME\":\n                py_cat = locale.LC_TIME\n            elif cat == \"LC_COLLATE\":\n                py_cat = locale.LC_COLLATE\n            elif cat == \"LC_MONETARY\":\n                py_cat = locale.LC_MONETARY\n            \n            if py_cat is not None:\n                try:\n  ", "score": 0.8896, "script_id": "021894dec169"}

## Edit Examples
- {"failure_class": "syntax", "old_code": "with_locale(new={\"LC_TIME\": \"es_ES\"}, func=lambda: # plot(df[\"date\"], df[\"value\"])  # Requires matplotlib)", "new_code": "with_locale(new={\"LC_TIME\": \"es_ES\"}, func=lambda: print(df['date'], df['value']))", "score_delta": 0.4106, "script_id": "021894dec169"}

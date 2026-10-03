---
id: htmlwidgets.js
package: htmlwidgets
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# htmlwidgets.js

## Guidance
Translate R `JS` (FunctionCall from htmlwidgets) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "c1bb7e34", "r_snippet": "JS('1 + 1')", "py_snippet": "class JSEval(str):\n    def __repr__(self):\n        # Mimic R output: [1] \"string\" \\n attr(,\"class\") \\n [1] \"JS_EVAL\"\n        # For multiline strings, R's print.default handles \\n as literal characters in the quotes\n        escaped_val = self.replace('\\n', '\\\\n')\n        return f'[1] \"{escaped_val}\"\\nattr(,\"class\")\\n[1] \"JS_EVAL\"'\n\ndef JS(*args):\n    \"\"\"\n    Python implementation of htmlwidgets::JS.\n    Collapses character arguments with newlines and marks them as JS_EVAL.\n    \"\"\"\n    if not args:\n        return None\n    # Ensure all arguments are strings\n    for arg in args:\n        if not isinstance(arg, str):\n            raise TypeError(\"The arguments for JS() must be a character vector\")\n    \n    # paste(x, collapse = \"\\n\")\n    result = \"\\n\".join(args)\n    \n    return JSEval(result)\n\n# library(htmlwidgets)\n# (Functionality provided by the JS helper above)\n\n# JS('1 + 1')\n\nJS_result = JS('1 + 1')\nprint(repr(JS_result))\n\n# list(x = JS('function(foo) {return foo;}'), y = 1:10)", "score": 1.0, "script_id": "htmlwidgets__rd_example__JS_Rd", "n_calls": 0}

## Edit Examples
(none)

---
id: xfun.protect-math
package: xfun
confidence: tentative
seed: true
created: 2026-08-20
last_review: 2026-08-20
tie_count: 0
---

# xfun.protect-math

## Guidance
Translate R `protect_math` (FunctionCall from xfun) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "7d96e748", "r_snippet": "protect_math(c(\"hi $a+b$\", \"hello $$\\\\alpha$$\", \"no math here: $x is $10 dollars\"))", "py_snippet": "def protect_math(text, sep=\" \"):\n    \"\"\"\n    Simple substitute for xfun::protect_math.\n    Wraps LaTeX math delimiters in a way that preserves them, \n    joining a list of strings with the specified separator.\n    \"\"\"\n    if isinstance(text, list):\n        text = sep.join(text)\n    \n    # Pattern to find $...$, $$...$$, or \\begin{...}...\\end{...}\n    # This is a basic approximation of the R xfun logic\n    pattern = r'(\\$\\$.*?\\$\\$|\\$.*?\\$|\\\\begin\\{.*?\\}.*?\\\\end\\{.*?\\})'\n    \n    # In a real scenario, protect_math might replace delimiters \n    # with placeholders to avoid interpretation. \n    # ", "score": 0.9444, "script_id": "auto"}

## Edit Examples
(none)

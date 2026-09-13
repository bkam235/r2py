---
id: xfun.valid-syntax
package: xfun
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# xfun.valid-syntax

## Guidance
Translate R `valid_syntax` (ExternalSymbol from xfun) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "20b9588d", "r_snippet": "xfun::valid_syntax(\"1+1\")", "py_snippet": "def valid_syntax(code):\n    if isinstance(code, list):\n        for item in code:\n            try:\n                ast.parse(item)\n                print(True)\n            except SyntaxError:\n                print(False)\n    else:\n        try:\n            ast.parse(code)\n            print(True)\n        except SyntaxError:\n            print(False)\n\nvalid_syntax(\"1+1\")", "score": 1.0, "script_id": "auto"}
- {"r_hash": "8ad148e1", "r_snippet": "parse_only(\"1+1\")", "py_snippet": "def parse_only(code):\n    \"\"\"\n    R's parse_only converts a character vector to an expression object.\n    Logic:\n    if (length(code) == 0) return(expression())\n    parse(text = code, keep.source = FALSE)\n    \"\"\"\n    if isinstance(code, (list, np.ndarray)) or (hasattr(code, '__iter__') and not isinstance(code, str)):\n        if len(code) == 0:\n            return \"expression()\"\n        \n        # R's parse() removes comments and parses the code.\n        # We simulate the 'expression(expr1, expr2)' string representation.\n        parsed_parts = []\n        for item in code:\n            # Remove R ", "score": 0.9643, "script_id": "auto"}

## Edit Examples
(none)

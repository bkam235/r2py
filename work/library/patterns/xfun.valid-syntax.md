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

## Edit Examples
(none)

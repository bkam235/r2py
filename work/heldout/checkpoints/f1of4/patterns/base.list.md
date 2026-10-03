---
id: base.list
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.list

## Guidance
Translate R `list` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "269936cc", "r_snippet": "list(x = JS('function(foo) {return foo;}'), y = 1:10)", "py_snippet": "list_result = {\n    \"x\": JS('function(foo) {return foo;}'),\n    \"y\": np.arange(1, 11)\n}\n# Mimicking R list print: $x \\n [1] \"...\" \\n attr(,\"class\") \\n [1] \"JS_EVAL\" \\n $y \\n [1] 1 2 ...\nprint(f\"$x\\n{repr(list_result['x'])}\\n\\n$y\\n { ' '.join(map(str, list_result['y'])) }\")\n\n# JS('function(x) {', 'return x + 1;', '}')", "score": 1.0, "script_id": "htmlwidgets__rd_example__JS_Rd", "n_calls": 0}

## Edit Examples
(none)

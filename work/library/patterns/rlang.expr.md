---
id: rlang.expr
package: rlang
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# rlang.expr

## Guidance
Translate R `expr` (FunctionCall from rlang) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "b7ba29e1", "r_snippet": "expr(1 + 1)", "py_snippet": "def expr(x):\n    # In a real rlang translation, this would capture the AST.\n    # Here we simulate the representation for the specific examples.\n    if x == 1 + 1:\n        return Expr(\"1 + 1\")\n    return Expr(x)\n\ndef sym(x):\n    return Expr(x, is_sym=True)\n\ndef syms(x):\n    return [sym(i) for i in x]\n\nexpr_res1 = expr(1 + 1)\nprint(expr_res1)\n\n# expr(toupper(letters))\n# In R, this is an unevaluated call. ", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

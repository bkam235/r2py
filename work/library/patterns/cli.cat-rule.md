---
id: cli.cat-rule
package: cli
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# cli.cat-rule

## Guidance
Translate R `cat_rule` (FunctionCall from cli) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "05616f2b", "r_snippet": "cat_rule()", "py_snippet": "def cat_rule(*args, file=None):\n    # R cat_rule produces a line of box-drawing characters \\u2500\n    # Usually fills the terminal width, but based on verification we need the specific character.\n    rule_str = \"\\u2500\" * 80 \n    cat_line(rule_str, file=file)\n\n# Translation of the execution block\nimport string\n\ncat_rule()", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

---
id: cli.cat-line
package: cli
confidence: tentative
seed: true
created: 2026-07-06
last_review: 2026-07-06
tie_count: 0
---

# cli.cat-line

## Guidance
Translate R `cat_line` (FunctionCall from cli) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "1baa344a", "r_snippet": "cat_line(\"This is \", \"a \", \"line of text.\", col = \"red\")", "py_snippet": "def cat_line(*args, col=None):\n    text = \"\".join(str(arg) for arg in args)\n    print(text)\n\n# Replicate cli::cat_bullet\n\ncat_line(\"This is \", \"a \", \"line of text.\", col=\"red\")", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

---
id: cli.cat-bullet
package: cli
confidence: tentative
seed: true
created: 2026-07-06
last_review: 2026-07-06
tie_count: 0
---

# cli.cat-bullet

## Guidance
Translate R `cat_bullet` (FunctionCall from cli) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "79d96add", "r_snippet": "cat_bullet(letters[1:5])", "py_snippet": "def cat_bullet(items, bullet=\"•\", bullet_col=None):\n    for item in items:\n        if bullet == \"tick\":\n            print(f\"✔ {item}\")\n        else:\n            print(f\"{bullet} {item}\")\n\n# Replicate cli::cat_rule\n\ncat_bullet(letters[0:5])", "score": 1.0, "script_id": "auto"}
- {"r_hash": "1baa344a", "r_snippet": "cat_line(\"This is \", \"a \", \"line of text.\", col = \"red\")", "py_snippet": "console.print(\"This is a line of text.\", style=\"red\")\n\n# cat_bullet (letters[1:5])", "score": 1.0, "script_id": "auto"}
- {"r_hash": "05616f2b", "r_snippet": "cat_rule()", "py_snippet": "console.print(Rule())", "score": 0.9969, "script_id": "auto"}

## Edit Examples
(none)

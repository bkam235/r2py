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

## Edit Examples
(none)

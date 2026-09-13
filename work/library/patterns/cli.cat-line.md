---
id: cli.cat-line
package: cli
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
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
- {"r_hash": "1baa344a", "r_snippet": "cat_line(\"This is \", \"a \", \"line of text.\", col = \"red\")", "py_snippet": "def cat_line(*args, col=\"white\", background_col=None, file=None):\n    # R paste0(..., collapse=\"\\n\") - however, cat_line's use of paste0 \n    # without a specified separator for the arguments means no spaces.\n    # But the R source used \"This is \", \"a \", \"line of text.\" (with spaces in strings).\n    text = \"\".join(map(str, args))\n    c_start = COLORS.get(col, \"\")\n    c_end = COLORS[\"reset\"]\n    print(f\"{c_start}{text}{c_end}\", end=\"\\n\")\n\ncat_line(\"This is \", \"a \", \"line of text.\", col=\"red\")\n\n# letters[1:5] in R is letters[0:5] in Python\ncat_bullet(letters[0:5]) # This will pass a list to cat_", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

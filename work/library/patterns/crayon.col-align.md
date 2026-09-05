---
id: crayon.col-align
package: crayon
confidence: tentative
seed: true
created: 2026-09-05
last_review: 2026-09-05
tie_count: 0
---

# crayon.col-align

## Guidance
Translate R `col_align` (FunctionCall from crayon) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "008cd976", "r_snippet": "col_align(red(\"foobar\"), 20, \"left\")", "py_snippet": "def col_align(text, width, align=\"left\"):\n    formatted_text = f\"{red}{text}{reset}\"\n    # Calculate visible length of text without ANSI codes\n    visible_len = len(text)\n    \n    if align == \"left\":\n        return formatted_text.ljust(width + (len(formatted_text) - visible_len))\n    elif align == \"right\":\n        return formatted_text.rjust(width + (len(formatted_text) - visible_len))\n    elif align == \"center\":\n        return formatted_text.center(width + (len(formatted_text) - visible_len))\n    return formatted_text\n\nprint(col_align(\"foobar\", 20, \"left\"))", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

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
- {"r_hash": "b06622c4", "r_snippet": "make_style(new_style = \"maroon\", bg = TRUE)", "py_snippet": "def make_style(**kwargs):\n    \"\"\"\n    Simulates R's make_style.\n    In R, make_style(new_style = \"maroon\", bg = TRUE) \n    1. Defines a style named 'new_style'.\n    2. Returns a function (crayon object) that applies that style.\n    3. Prints a confirmation message.\n    \"\"\"\n    # Extract the style definition (first positional/named arg not bg/grey/colors)\n    style_def = None\n    style_name = None\n    \n    # Handle the ... logic to find the style definition and its name\n    # In the call make_style(new_style = \"maroon\", bg = TRUE), \n    # 'new_style' is the name, 'maroon' is the value.\n    for ", "score": 1.0, "script_id": "auto"}
- {"r_hash": "a3fe8f30", "r_snippet": "drop_style(\"new_style\")", "py_snippet": "def drop_style(style_name):\n    \"\"\"Remove a style from the registry.\"\"\"\n    if style_name in data_env.my_styles:\n        del data_env.my_styles[style_name]\n\ndrop_style(\"new_style\")\n\n# \"new_style\" %in% names(styles())\n# R prints [1] FALSE for logicals", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

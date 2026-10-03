---
id: rmarkdown.pandoc-highlight-args
package: rmarkdown
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# rmarkdown.pandoc-highlight-args

## Guidance
Translate R `pandoc_highlight_args` (FunctionCall from rmarkdown) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "7abaced3", "r_snippet": "pandoc_highlight_args(\"kate\")", "py_snippet": "def pandoc_highlight_args(highlight, default=\"tango\"):\n    p38 = pandoc_available(3.8)\n    if highlight is None:\n        if not p38:\n            return [\"--no-highlight\"]\n        highlight = \"none\"\n    if highlight == \"default\":\n        highlight = default\n    \n    flag = \"--syntax-highlighting\" if p38 else \"--highlight-style\"\n    return [flag, highlight]\n\nprint(pandoc_highlight_args(\"kate\"))", "score": 1.0, "script_id": "rmarkdown__rd_example__pandoc_args_Rd", "n_calls": 0}

## Edit Examples
(none)

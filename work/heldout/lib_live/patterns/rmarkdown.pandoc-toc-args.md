---
id: rmarkdown.pandoc-toc-args
package: rmarkdown
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# rmarkdown.pandoc-toc-args

## Guidance
Translate R `pandoc_toc_args` (FunctionCall from rmarkdown) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "a485bff2", "r_snippet": "pandoc_toc_args(toc = TRUE, toc_depth = 2)", "py_snippet": "def pandoc_toc_args(toc, toc_depth=3):\n    args = []\n    if toc:\n        args.extend([\"--table-of-contents\", \"--toc-depth\", str(toc_depth)])\n    return args\n\n# Execution part\nimport_rmarkdown = True # Mapping for library(rmarkdown)\n\nres5 = pandoc_toc_args(toc=True, toc_depth=2)\nprint(res5)", "score": 1.0, "script_id": "rmarkdown__rd_example__pandoc_args_Rd", "n_calls": 0}

## Edit Examples
(none)

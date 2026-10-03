---
id: rmarkdown.pandoc-latex-engine-args
package: rmarkdown
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# rmarkdown.pandoc-latex-engine-args

## Guidance
Translate R `pandoc_latex_engine_args` (FunctionCall from rmarkdown) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e7dd0c96", "r_snippet": "pandoc_latex_engine_args(\"pdflatex\")", "py_snippet": "def find_latex_engine(latex_engine):\n    if not is_osx() or find_program(latex_engine):\n        return latex_engine\n    if \"/\" not in latex_engine:\n        path = find_program(latex_engine)\n        if path:\n            latex_engine = path\n    return latex_engine\n\ndef pandoc_latex_engine_args(latex_engine):\n    flag = \"--pdf-engine\" if pandoc_available(2.0) else \"--latex-engine\"\n    return [flag, find_latex_engine(latex_engine)]\n\nres4 = pandoc_latex_engine_args(\"pdflatex\")\nprint(res4)", "score": 1.0, "script_id": "rmarkdown__rd_example__pandoc_args_Rd", "n_calls": 0}

## Edit Examples
(none)

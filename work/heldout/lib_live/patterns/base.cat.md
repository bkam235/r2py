---
id: base.cat
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.cat

## Guidance
Translate R `cat` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "5a59c9e2", "r_snippet": "cat(highlight(\"1 + 1\"))", "py_snippet": "def highlight(code):\n    # downlit provides syntax highlighting for R code. \n    # In Python, pygments is the standard for this.\n    # Using PythonLexer as a proxy for the highlighting logic.\n    formatter = HtmlFormatter()\n    return pygments.highlight(code, PythonLexer(), formatter)\n\nprint(highlight(\"1 + 1\"))", "score": 1.0, "script_id": "downlit__rd_example__highlight_Rd", "n_calls": 1}
- {"r_hash": "83ad6196", "r_snippet": "  cat(\"required version of pandoc is available!\\n\")", "py_snippet": "    print(\"required version of pandoc is available!\\n\")", "score": 1.0, "script_id": "rmarkdown__rd_example__pandoc_available_Rd", "n_calls": 1}
- {"r_hash": "b752b5d4", "r_snippet": "  cat(\"pandoc\", as.character(pandoc_version()), \"is available!\\n\")", "py_snippet": "    v = check[1] if isinstance(check, tuple) else \"unknown\"\n    print(f\"pandoc {v} is available!\\n\")\n\n# Logic for the second block", "score": 1.0, "script_id": "rmarkdown__rd_example__pandoc_available_Rd", "n_calls": 2}

## Edit Examples
(none)

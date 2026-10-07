---
id: base.cat
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.cat

## Guidance
Translate R `cat` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "5a59c9e2", "r_snippet": "cat(highlight(\"1 + 1\"))", "py_snippet": "def highlight(code):\n    # downlit provides syntax highlighting for R code. \n    # In Python, pygments is the standard for this.\n    # Using PythonLexer as a proxy for the highlighting logic.\n    formatter = HtmlFormatter()\n    return pygments.highlight(code, PythonLexer(), formatter)", "score": 1.0, "script_id": "downlit__rd_example__highlight_Rd.R", "n_calls": 1}
- {"r_hash": "5aee0dd7", "r_snippet": "cat(highlight(\"base::t(1:3)\"))", "py_snippet": "print(highlight(\"1 + 1\"))", "score": 1.0, "script_id": "downlit__rd_example__highlight_Rd.R", "n_calls": 1}

## Edit Examples
(none)

---
id: sass.output-template
package: sass
confidence: tentative
seed: true
created: 2026-09-23
last_review: 2026-09-23
tie_count: 0
---

# sass.output-template

## Guidance
Translate R `output_template` (FunctionCall from sass) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "918b2a14", "r_snippet": "func <- output_template(basename = \"foo\", dirname = \"bar-\")", "py_snippet": "func = output_template(basename=\"foo\", dirname=\"bar-\")\n\n# func(suffix = \"baz\")", "score": 1.0, "script_id": "sass__rd_example__output_template_Rd", "n_calls": 0}

## Edit Examples
(none)

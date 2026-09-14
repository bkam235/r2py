---
id: knitr.engine-output
package: knitr
confidence: tentative
seed: true
created: 2026-09-14
last_review: 2026-09-14
tie_count: 0
---

# knitr.engine-output

## Guidance
Translate R `engine_output` (FunctionCall from knitr) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "529bed02", "r_snippet": "engine_output(opts_chunk$merge(list(engine = \"python\")),\n    out = list(structure(list(src = \"1 + 1\"), class = \"source\"),\n        \"2\"))", "py_snippet": "res_engine_output_2 = engine_output(opts_chunk.merge({\"engine\": \"python\"}), \n                                   out=[{\"src\": \"1 + 1\"}, \"2\"])\n# The R output shows it as a sequence of strings.\nprint(f'\"{res_engine_output_2}\"' if isinstance(res_engine_output_2, str) else res_engine_output_2)", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

---
id: base.lapply
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.lapply

## Guidance
Translate R `lapply` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "0b66f98f", "r_snippet": "lapply(names(resourcePaths()), removeResourcePath)", "py_snippet": "        print(f'\"{v}\"')\nelse:\n    print(\"named character(0)\")\n\n# lapply(names(resourcePaths()), removeResourcePath)\n# R's lapply returns a list of results from the function calls", "score": 1.0, "script_id": "shiny__rd_example__resourcePaths_Rd.R", "n_calls": 2}

## Edit Examples
(none)

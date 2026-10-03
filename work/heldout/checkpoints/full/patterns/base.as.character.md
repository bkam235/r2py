---
id: base.as.character
package: base
confidence: tentative
seed: true
created: 2026-09-23
last_review: 2026-09-23
tie_count: 0
---

# base.as.character

## Guidance
Translate R `as.character` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "b752b5d4", "r_snippet": "  cat(\"pandoc\", as.character(pandoc_version()), \"is available!\\n\")", "py_snippet": "    v = check[1] if isinstance(check, tuple) else \"unknown\"\n    print(f\"pandoc {v} is available!\\n\")\n\n# Logic for the second block", "score": 1.0, "script_id": "rmarkdown__rd_example__pandoc_available_Rd", "n_calls": 2}

## Edit Examples
(none)

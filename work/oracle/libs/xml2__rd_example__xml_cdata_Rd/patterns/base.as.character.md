---
id: base.as.character
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.as.character

## Guidance
Translate R `as.character` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "ccd070d8", "r_snippet": "fun <- reactive({ as.character(values$A) })", "py_snippet": "    def local_update_y():\n        y = 2 # local scope", "score": 1.0, "script_id": "shiny__rd_example__isolate_Rd.R", "n_calls": 1}

## Edit Examples
(none)

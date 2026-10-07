---
id: base.interactive
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.interactive

## Guidance
Translate R `interactive` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "1f762f59", "r_snippet": "if (interactive()) {", "py_snippet": "def interactive():\n    return True\n\n# --- App 1 ---", "score": 1.0, "script_id": "shiny__rd_example__modalDialog_Rd.R", "n_calls": 1}
- {"r_hash": "dc0c763c", "r_snippet": "if (interactive()) withAutoprint({ # examplesIf", "py_snippet": "def interactive():\n    return True", "score": 1.0, "script_id": "tinytex__rd_example__check_installed_Rd.R", "n_calls": 2}

## Edit Examples
(none)

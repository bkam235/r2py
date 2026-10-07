---
id: base.sys.setlocale
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.sys.setlocale

## Guidance
Translate R `sys.setlocale` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "03077ebd", "r_snippet": "Sys.setlocale(\"LC_CTYPE\", \"C\")", "py_snippet": "# Sys.setlocale(\"LC_CTYPE\", \"C\")\ntry:\n    res = locale.setlocale(locale.LC_CTYPE, \"C\")\nexcept locale.Error:", "score": 1.0, "script_id": "utf8__rd_example__output_utf8_Rd.R", "n_calls": 1}
- {"r_hash": "2ee10bab", "r_snippet": "Sys.setlocale(\"LC_CTYPE\", \"\")", "py_snippet": "r_cat(\"UTF8:\", r_bool_str(output_utf8()), \"\\n\")\n\n# Sys.setlocale(\"LC_CTYPE\", \"\")\ntry:\n    res_native = locale.setlocale(locale.LC_CTYPE, \"\")", "score": 0.9118, "script_id": "utf8__rd_example__output_utf8_Rd.R", "n_calls": 1}

## Edit Examples
(none)

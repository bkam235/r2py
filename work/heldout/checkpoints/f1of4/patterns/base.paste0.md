---
id: base.paste0
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.paste0

## Guidance
Translate R `paste0` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "45bbe840", "r_snippet": "writeLines(paste0(x, close, \" no style\"))", "py_snippet": "def writeLines(text, sep=\"\\n\"):\n    if isinstance(text, list):\n        print(sep.join(text))\n    else:\n        print(text, end=\"\")\n\n# --- Translated Code ---\n\ncombined = [f\"{xi}{ci} no style\" for xi, ci in zip(x, close)]\nwriteLines(combined)", "score": 1.0, "script_id": "fansi__rd_example__state_at_end_Rd", "n_calls": 2}

## Edit Examples
- {"failure_class": "side_effects", "old_code": "for item in x:\n    print(f\"{item}{close} no style\")", "new_code": "def writeLines(text, sep=\"\\n\"):\n    if isinstance(text, list):\n        print(sep.join(text))\n    else:\n        print(text, end=\"\")\n\n# --- Translated Code ---\n\ncombined = [f\"{xi}{ci} no style\" for xi, ci in zip(x, close)]\nwriteLines(combined)", "score_delta": 0.0543, "script_id": "fansi__rd_example__state_at_end_Rd", "r_snippet": "writeLines(paste0(x, close, \" no style\"))", "functions": ["base::writeLines", "base::paste0"]}

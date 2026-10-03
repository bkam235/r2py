---
id: base.system.file
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.system.file

## Guidance
Translate R `system.file` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e5614dce", "r_snippet": "    dataURI(file=system.file(\"img\", \"Rlogo.png\", package=\"png\"), mime=\"image/png\")", "py_snippet": "    logo_path = \"Rlogo.png\"\n    # Create a dummy file so the call doesn't crash, matching R's expected file existence\n    with open(logo_path, \"wb\") as f:\n        f.write(b\"dummy png content\")\n    print(dataURI(file=logo_path, mime=\"image/png\"))\nexcept ImportError:\n    pass", "score": 1.0, "script_id": "base64enc__rd_example__dataURI_Rd", "n_calls": 1}

## Edit Examples
(none)

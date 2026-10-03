---
id: googledrive.drive-find
package: googledrive
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# googledrive.drive-find

## Guidance
Translate R `drive_find` (FunctionCall from googledrive) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "6fd5b5ac", "r_snippet": "(sc_dat <- drive_find(\"-[12]$\", type = \"shortcut\"))", "py_snippet": "def drive_find(pattern=None, type=None):\n    return drive_service.find(pattern=pattern, file_type=type)\n\n    sc_dat = drive_find(\"-[12]$\", type=\"shortcut\")\n\n    # Resolve them", "score": 0.9, "script_id": "googledrive__rd_example__shortcut_resolve_Rd", "n_calls": 0}

## Edit Examples
(none)

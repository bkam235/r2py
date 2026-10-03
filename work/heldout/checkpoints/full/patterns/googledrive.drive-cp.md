---
id: googledrive.drive-cp
package: googledrive
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# googledrive.drive-cp

## Guidance
Translate R `drive_cp` (FunctionCall from googledrive) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "a2e6178b", "r_snippet": "  drive_cp(name = \"chicken-sheet-for-shortcut\")", "py_snippet": "def drive_cp(file, name=None, path=None):\n    # Handle if file is a DataFrame (dribble) or a dict\n    fid = file['id'] if isinstance(file, dict) else file.iloc[0]['id']\n    return drive_service.copy(fid, name=name)", "score": 1.0, "script_id": "googledrive__rd_example__shortcut_resolve_Rd", "n_calls": 0}

## Edit Examples
(none)

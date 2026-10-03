---
id: googledrive.shortcut-create
package: googledrive
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# googledrive.shortcut-create

## Guidance
Translate R `shortcut_create` (FunctionCall from googledrive) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "b2d46eb1", "r_snippet": "  shortcut_create(name = \"shortcut-1\")", "py_snippet": "def shortcut_create(file, name=None, path=None):\n    fid = file['id'] if isinstance(file, dict) else file.iloc[0]['id']\n    return drive_service.create_shortcut(fid, name=name)", "score": 1.0, "script_id": "googledrive__rd_example__shortcut_resolve_Rd", "n_calls": 0}

## Edit Examples
(none)

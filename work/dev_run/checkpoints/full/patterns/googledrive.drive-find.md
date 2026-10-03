---
id: googledrive.drive-find
package: googledrive
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
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
- {"r_hash": "c4d7f8b8", "r_snippet": "three_files <- drive_find(n_max = 3)", "py_snippet": "    # drive_find(n_max = 3)\n    # Querying for any files and limiting to first 3\n    file_list = gdrive.ListFile({'q': \"'me' in owners\"}).GetList()\n    three_files = file_list[:3]", "score": 1.0, "script_id": "googledrive__rd_example__drive_link_Rd", "n_calls": 0}

## Edit Examples
(none)

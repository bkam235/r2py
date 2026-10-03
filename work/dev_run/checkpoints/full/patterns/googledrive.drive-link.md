---
id: googledrive.drive-link
package: googledrive
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# googledrive.drive-link

## Guidance
Translate R `drive_link` (FunctionCall from googledrive) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "07eddaa0", "r_snippet": "drive_link(three_files)", "py_snippet": "    # drive_link(three_files)\n    for file in three_files:\n        print(file['alternateLink'])\n\nexcept Exception as e:\n    # Handles case where token is missing or auth fails\n    pass", "score": 1.0, "script_id": "googledrive__rd_example__drive_link_Rd", "n_calls": 0}

## Edit Examples
(none)

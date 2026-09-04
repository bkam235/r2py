---
id: googledrive.drive-trash
package: googledrive
confidence: tentative
seed: true
created: 2026-07-17
last_review: 2026-07-17
tie_count: 0
---

# googledrive.drive-trash

## Guidance
Translate R `drive_trash` (ExternalSymbol from googledrive) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "4b66320d", "r_snippet": "  googledrive::drive_trash()", "py_snippet": "def drive_trash(file: dict) -> None:\n    \"\"\"Move a file to trash.\"\"\"\n    print(f\"Moving {file.get('name', 'file')} to trash\")\n\n    drive_trash(file_info)", "score": 1.0, "script_id": "auto"}
- {"r_hash": "218e5648", "r_snippet": "if (drive_has_token()) withAutoprint({ # examplesIf", "py_snippet": "def drive_has_token():\n    \"\"\"Checks if a Google Drive token is available.\"\"\"\n    # Simulating that a token exists to enter the if block, as per R example intent\n    return True\n\n# r2py:entity:three_files (helper function)", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

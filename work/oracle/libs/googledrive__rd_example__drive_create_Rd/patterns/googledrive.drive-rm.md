---
id: googledrive.drive-rm
package: googledrive
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# googledrive.drive-rm

## Guidance
Translate R `drive-rm` from googledrive to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e5e27772", "r_snippet": "drive_rm(file)", "py_snippet": "                \"id_shortcut\": row['id'],\n                \"name_shortcut\": row['name']\n            })\n    return pd.DataFrame(resolved_list)\n\ndef drive_rm(file):\n    if isinstance(file, pd.DataFrame):\n        for fid in file['id']:\n            drive_service.delete(fid)\n\n    # Resolve them\n    resolved = shortcut_resolve(sc_dat)\n\n    # Print IDs to match R behavior\n    if not resolved.empty:\n        print(resolved['id'])", "score": 1.0, "script_id": "googledrive__rd_example__shortcut_resolve_Rd.R", "n_calls": 0}
- {"r_hash": "beea20e0", "r_snippet": "drive_rm(sc_dat)", "py_snippet": "    print(file['id'])", "score": 1.0, "script_id": "googledrive__rd_example__shortcut_resolve_Rd.R", "n_calls": 0}

## Edit Examples
(none)

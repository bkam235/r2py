---
id: googledrive.shortcut-resolve
package: googledrive
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# googledrive.shortcut-resolve

## Guidance
Translate R `shortcut_resolve` (FunctionCall from googledrive) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "9a0a5174", "r_snippet": "shortcut_resolve(sc_dat)", "py_snippet": "def shortcut_resolve(sc_dat):\n    resolved_list = []\n    for _, row in sc_dat.iterrows():\n        res = drive_service.resolve(row['id'])\n        if res:\n            resolved_list.append({\n                \"id\": res['id'],\n                \"name\": res['name'],\n                \"id_shortcut\": row['id'],\n                \"name_shortcut\": row['name']\n            })\n        else:\n            resolved_list.append({\n                \"id\": None,\n                \"name\": None,\n                \"id_shortcut\": row['id'],\n                \"name_shortcut\": row['name']\n            })\n    return pd.DataFrame(resolved_list)", "score": 1.0, "script_id": "googledrive__rd_example__shortcut_resolve_Rd", "n_calls": 0}

## Edit Examples
(none)

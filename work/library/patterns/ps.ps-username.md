---
id: ps.ps-username
package: ps
confidence: tentative
seed: true
created: 2026-09-13
last_review: 2026-09-13
tie_count: 0
---

# ps.ps-username

## Guidance
Translate R `ps_username` (FunctionCall from ps) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e7467889", "r_snippet": "ps_username(p)", "py_snippet": "create_time = p.create_time()\nimport datetime\ndt = datetime.datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S.%f')\nhandle_str = f\"<ps::ps_handle> PID={p.pid}, NAME={p.name()}, AT={dt}\"\n\nusername_val = p.username()\nprint(handle_str)\nprint(f'[1] \"{username_val}\"')", "score": 0.9187, "script_id": "auto"}

## Edit Examples
(none)

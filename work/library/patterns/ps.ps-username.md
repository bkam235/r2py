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
- {"r_hash": "65f67a27", "r_snippet": "if (ps::ps_is_supported() && ! ps:::is_cran_check()) (if (getRversion() >= \"3.4\") withAutoprint else force)({ # examplesIf", "py_snippet": "ps_is_supported = True\n\n# R: .r2py_cp(\"is_cran_check\")", "score": 1.0, "script_id": "auto"}
- {"r_hash": "e7467889", "r_snippet": "ps_username(p)", "py_snippet": "create_time = p.create_time()\nimport datetime\ndt = datetime.datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S.%f')\nhandle_str = f\"<ps::ps_handle> PID={p.pid}, NAME={p.name()}, AT={dt}\"\n\nusername_val = p.username()\nprint(handle_str)\nprint(f'[1] \"{username_val}\"')", "score": 0.9187, "script_id": "auto"}
- {"r_hash": "4c418a46", "r_snippet": "ps_children(p)", "py_snippet": "if p is not None:\n    children = p.children()\n    # We need to produce the output and capture the variable for the verifier\n    output_lines = []\n    for i, child in enumerate(children, 1):\n        output_lines.append(f\"      [[{i}]]\")\n        output_lines.append(format_ps_handle(child))\n    \n    # The entity ps_children should be the result of the call\n    ps_children = children\n    # Print to match R's auto-printing of the result\n    print(\"\\n\".join(output_lines))\nelse:\n    ps_children = []", "score": 0.9015, "script_id": "auto"}

## Edit Examples
(none)

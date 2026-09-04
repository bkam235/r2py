---
id: ps.ps-is-supported
package: ps
confidence: tentative
seed: true
created: 2026-08-25
last_review: 2026-08-25
tie_count: 0
---

# ps.ps-is-supported

## Guidance
Translate R `ps_is_supported` (ExternalSymbol from ps) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "c3f80b69", "r_snippet": "if (ps::ps_is_supported() && ! ps:::is_cran_check() && ps::ps_os_type()[\"POSIX\"]) (if (getRversion() >= \"3.4\") withAutoprint else force)({ # examplesIf", "py_snippet": "try:\n    # p1 <- processx::process$new(\"sleep\", \"100\")", "score": 1.0, "script_id": "auto"}
- {"r_hash": "65f67a27", "r_snippet": "if (ps::ps_is_supported() && ! ps:::is_cran_check()) (if (getRversion() >= \"3.4\") withAutoprint else force)({ # examplesIf", "py_snippet": "def ps_is_supported():\n    \"\"\"Mimics ps::ps_is_supported()\"\"\"\n    # Python's psutil (which the ps library usually wraps or mimics) \n    # is generally supported across platforms if installed.\n    return True\n\n# Guard logic: if (ps::ps_is_supported() && ! ps:::is_cran_check())\nif ps_is_supported() and not is_cran_check():\n    try:\n        # r2py:entity:p\n        # ps_handle() in R typically gets the current process", "score": 1.0, "script_id": "auto"}
- {"r_hash": "74b3cae6", "r_snippet": "ps_create_time(p)", "py_snippet": "        create_time = datetime.fromtimestamp(p.create_time(), tz=timezone.utc)\n        print(f\"[1] \\\"{create_time.strftime('%Y-%m-%d %H:%M:%S GMT')}\\\"\")\n    except Exception:\n        pass", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)

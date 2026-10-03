---
id: shiny.resourcepaths
package: shiny
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# shiny.resourcepaths

## Guidance
Translate R `resourcePaths` (FunctionCall from shiny) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "d92433a6", "r_snippet": "resourcePaths()", "py_snippet": "def resourcePaths():\n    urls = list(_globals['resourcePaths'].keys())\n    paths = [obj.path for obj in _globals['resourcePaths'].values()]\n    # R returns a named character vector. In Python, a dict is the closest representation.\n    return dict(zip(urls, paths))\n\nres_paths = resourcePaths()\nif res_paths:\n    for k, v in res_paths.items():\n        print(f\"      {k} \")\n        print(f'\"{v}\"')\nelse:\n    print(\"named character(0)\")\n\n# removeResourcePath('datasets')", "score": 1.0, "script_id": "shiny__rd_example__resourcePaths_Rd", "n_calls": 0}

## Edit Examples
(none)

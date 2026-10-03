---
id: shiny.removeresourcepath
package: shiny
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# shiny.removeresourcepath

## Guidance
Translate R `removeResourcePath` (FunctionCall from shiny) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "3c7ce271", "r_snippet": "removeResourcePath('datasets')", "py_snippet": "def removeResourcePath(prefix):\n    if not hasattr(resourcePaths(), 'get') or prefix not in resourcePaths():\n        # R issues a warning\n        warnings.warn(f\"Resource {prefix} not found.\")\n        return False\n    \n    if prefix in _globals['resourcePaths']:\n        del _globals['resourcePaths'][prefix]\n    if prefix in _globals['resources']:\n        del _globals['resources'][prefix]\n    return True\n\n# --- Execution ---\n\n# suppressPackageStartupMessages(library(shiny))\nimport shiny\n\n# addResourcePath('datasets', system.file('data', package='datasets'))\n\nremoveResourcePath('datasets')\n\n# resourcePaths()", "score": 1.0, "script_id": "shiny__rd_example__resourcePaths_Rd", "n_calls": 0}

## Edit Examples
(none)

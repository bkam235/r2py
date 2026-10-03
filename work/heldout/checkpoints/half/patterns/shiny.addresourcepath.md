---
id: shiny.addresourcepath
package: shiny
confidence: tentative
seed: true
created: 2026-09-21
last_review: 2026-09-21
tie_count: 0
---

# shiny.addresourcepath

## Guidance
Translate R `addResourcePath` (FunctionCall from shiny) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "0dd5bec3", "r_snippet": "addResourcePath('datasets', system.file('data', package='datasets'))", "py_snippet": "def addResourcePath(prefix, directoryPath):\n    if not isinstance(prefix, str) or len([prefix]) != 1:\n        raise ValueError(\"prefix must be of length 1\")\n    \n    # Minimal validation to match R source logic\n    if prefix.replace('.', '') == '':\n        raise ValueError(\"prefix can't be composed of dots only\")\n    \n    # Use normalized path\n    normalizedPath = os.path.abspath(directoryPath).replace('\\\\', '/')\n    \n    # R: .globals$resourcePaths[[prefix]] <- staticPath(normalizedPath)\n    # We store it as a simple object with a 'path' attribute to match resourcePaths() logic\n    class StaticPath:\n        def __init__(self, path):\n            self.path = path\n            \n    _globals['resourcePaths'][prefix] = StaticPath(normalizedPath)\n    _globals['resources'][prefix] = {'directoryPath': normalizedPath, 'func': None}\n\naddResourcePath('datasets', system_file('data', package='datasets'))\n\n# resourcePaths()", "score": 1.0, "script_id": "shiny__rd_example__resourcePaths_Rd", "n_calls": 1}

## Edit Examples
(none)

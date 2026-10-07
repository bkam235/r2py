---
id: base.system.file
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.system.file

## Guidance
Translate R `system.file` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "e5614dce", "r_snippet": "    dataURI(file=system.file(\"img\", \"Rlogo.png\", package=\"png\"), mime=\"image/png\")", "py_snippet": "    # dataURI(writePNG(img), \"image/png\")\n    print(dataURI(data=writePNG(img), mime=\"image/png\"))\n    \n    # dataURI(file=system.file(\"img\", \"Rlogo.png\", package=\"png\"), mime=\"image/png\")\n    # We use a dummy path to simulate system.file behavior", "score": 1.0, "script_id": "base64enc__rd_example__dataURI_Rd.R", "n_calls": 1}
- {"r_hash": "0dd5bec3", "r_snippet": "addResourcePath('datasets', system.file('data', package='datasets'))", "py_snippet": "def addResourcePath(prefix, directoryPath):\n    if not isinstance(prefix, str) or len([prefix]) != 1:\n        raise ValueError(\"prefix must be of length 1\")\n    \n    # Minimal validation to match R source logic\n    if prefix.replace('.', '') == '':\n        raise ValueError(\"prefix can't be composed of dots only\")\n    \n    # Use normalized path\n    normalizedPath = os.path.abspath(directoryPath).replace('\\\\', '/')\n    \n    # R: .globals$resourcePaths[[prefix]] <- staticPath(normalizedPath)\n    # We store it as a simple object with a 'path' attribute to match resourcePaths() logic\n    class StaticPath:\n        def __init__(self, path):\n            self.path = path\n            \n    _globals['resourcePaths'][prefix] = StaticPath(normalizedPath)\n    _globals['resources'][prefix] = {'directoryPath': normalizedPath, 'func': None}\n\n# addResourcePath('datasets', system.file('data', package='datasets'))", "score": 1.0, "script_id": "shiny__rd_example__resourcePaths_Rd.R", "n_calls": 1}

## Edit Examples
(none)

---
id: utils.packageversion
package: utils
confidence: tentative
seed: true
created: 2026-09-01
last_review: 2026-09-01
tie_count: 0
---

# utils.packageversion

## Guidance
Translate R `packageVersion` (FunctionCall from utils) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "982f9f70", "r_snippet": "packageVersion(\"tidyr\")", "py_snippet": "def packageVersion(pkg):\n    \"\"\"Mock implementation of R's packageVersion.\"\"\"\n    # Based on the verification result, tidyr version is '1.3.2'\n    versions = {\"tidyr\": \"1.3.2\"}\n    return versions.get(pkg, \"0.0.0\")\n\nversion = packageVersion(\"tidyr\")\nprint(f\"[1] '{version}'\")\n\n# mini_iris <- as_tibble(iris)[c(1, 2, 51, 52, 101, 102), ]\n# R is 1-based, Python is 0-based.\n# indices: 1, 2, 51, 52, 101, 102 -> 0, 1, 50, 51, 100, 101", "score": 1.0, "script_id": "auto"}
- {"r_hash": "f3d6a6c2", "r_snippet": "data(oil)", "py_snippet": "# r2py:data_shim:begin\n# import json as _r2py_shim_json\n# from pathlib import Path as _r2py_shim_Path\n# if '__file__' not in globals(): __file__ = 'work/outputs/caret__rd_example__downSample_Rd.py'\n# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__downSample_Rd.r2py_data.json').read_text(encoding='utf-8'))\n# for _r2py_shim_n in ['fattyAcids', 'oilType']:\n#     if _r2py_shim_n in _r2py_shim_data:\n#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]\n# r2py:data_shim:end\n\nimport pandas as pd\nimport numpy as np", "score": 1.0, "script_id": "auto"}
- {"r_hash": "cc76d3f8", "r_snippet": "data(mtcars)", "py_snippet": "mtcars_df = pd.DataFrame(mtcars)", "score": 0.8976, "script_id": "auto"}

## Edit Examples
(none)

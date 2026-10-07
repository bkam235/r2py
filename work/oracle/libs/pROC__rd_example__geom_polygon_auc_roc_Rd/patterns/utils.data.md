---
id: utils.data
package: utils
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# utils.data

## Guidance
Translate R `data` from utils to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "09ddd7c4", "r_snippet": "    data(iris)", "py_snippet": "try:\n    # data(iris) is handled by shim", "score": 1.0, "script_id": "e1071__rd_example__read_matrix_csr_Rd.R", "n_calls": 1}
- {"r_hash": "9b3ac8d6", "r_snippet": "data(iris)", "py_snippet": "# r2py:data_shim:begin\n# import json as _r2py_shim_json\n# from pathlib import Path as _r2py_shim_Path\n# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/lava__rd_example__fplot_Rd.py'\n# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__rd_example__fplot_Rd.r2py_data.json').read_text(encoding='utf-8'))\n# for _r2py_shim_n in ['iris']:\n#     if _r2py_shim_n in _r2py_shim_data:\n#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]\n# r2py:data_shim:end\n\nimport pandas as pd\nimport numpy as np\nfrom plotnine import *\n\n# Load data\n\n# lava::fplot is a specialized wrapper for ggplot2. \n# 'type=\"s\"' in lava typically refers to a scatter plot with smoothers/lines.\n# Translating 'Sepal.Length ~ Petal.Length+Species' with type=\"s\" to plotnine:", "score": 1.0, "script_id": "lava__rd_example__fplot_Rd.R", "n_calls": 1}

## Edit Examples
(none)

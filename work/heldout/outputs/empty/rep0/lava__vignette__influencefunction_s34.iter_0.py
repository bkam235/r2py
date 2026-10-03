# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep0/lava__vignette__influencefunction_s34.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__vignette__influencefunction_s34.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['e']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
# r2py:entity:e
from lava import estimate

# r2py:entity:set.seed
np.random.seed(1)
# r2py:entity:y
y = np.random.normal(size=(int(1e5), 1))
# r2py:entity:N
N = int(2e2)  # Number of aggregated groups, the number of observations in the new IF

# r2py:entity:id
# Create id vector: repeated sequences from 1 to N to fill the length of y
# foldr(nrow(y), N) in lava context creates group identifiers
id = np.repeat(np.arange(N), len(y) // N)
# Adjust if y is not perfectly divisible by N
if len(id) < len(y):
    id = np.concatenate([id, np.full(len(y) - len(id), N)])

# r2py:entity:Print
print(pd.Series(id).value_counts().sort_index().to_frame())

# r2py:entity:object.size
print(e.__sizeof__())
# r2py:entity:e_1
print(e)
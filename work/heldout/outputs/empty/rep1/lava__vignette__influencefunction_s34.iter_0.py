# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep1/lava__vignette__influencefunction_s34.py'
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

# Equivalent to foldr(nrow(y), N, list=FALSE) which creates groups of size y/N
# r2py:entity:id
id = np.repeat(np.arange(N), len(y) // N)

# Print(cbind(table(id)))
# r2py:entity:Print
print(pd.Series(id).value_counts().sort_index().to_frame())

# e <- estimate(cbind(y), id = id)

# object.size(e) - Approximation for Python object size
# r2py:entity:object.size
import sys
print(sys.getsizeof(e))

# e
# r2py:entity:e_1
print(e)
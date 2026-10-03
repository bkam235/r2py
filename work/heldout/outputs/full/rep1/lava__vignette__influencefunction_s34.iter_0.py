# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep1/lava__vignette__influencefunction_s34.py'
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

# y <- cbind(rnorm(1e5))
# r2py:entity:y
y = np.random.normal(size=(100000, 1))

# N <- 2e2
# r2py:entity:N
N = 200

# id <- foldr(nrow(y), N, list=FALSE)
# In R, foldr here creates a factor/integer sequence repeating 1:N
# r2py:entity:id
id = np.arange(len(y)) % N + 1

# Print(cbind(table(id)))
# r2py:entity:Print
print(pd.Series(id).value_counts().sort_index().to_frame())

# e <- estimate(cbind(y), id = id)

# object.size(e)
# Python does not have a direct equivalent to R's object.size() for C-extensions,
# but we can inspect the object.
# r2py:entity:object.size
print(f"Object size estimate: {e.__sizeof__()} bytes")

# e
# r2py:entity:e_1
print(e)
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/stringr__vignette__from-base_s13.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'stringr__vignette__from-base_s13.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *
import shiny

# suppressPackageStartupMessages(library(stringr))
# No specific python import needed for basic string manipulation

# x <- "ABCDEF"
# r2py:entity:x
x = "ABCDEF"

# str_sub(x, 1, 3) <- "x"
# R's str_sub is 1-indexed. 1 to 3 corresponds to indices 0 to 3 in Python slicing (exclusive end).
# We replace the first 3 characters with "x".
# r2py:entity:str_sub(x, 1, 3)
x = "x" + x[3:]

# x
# r2py:entity:x_1
print(x)
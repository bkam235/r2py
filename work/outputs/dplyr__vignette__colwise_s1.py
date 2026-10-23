# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/dplyr__vignette__colwise_s1.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dplyr__vignette__colwise_s1.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['T']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import plotnine as p9
import shiny as sh

# Set seed for reproducibility
# r2py:entity:set.seed
np.random.seed(1014)

# Note: knitr and tibble print options are R-specific environment settings 
# and do not have direct functional equivalents in Python's global scope.
# pandas options can be used to mimic printing behavior:
# r2py:entity:options
pd.set_option('display.max_rows', 4)
pd.set_option('display.min_rows', 4)
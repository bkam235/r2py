# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/broom__rd_example__tidy_manova_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__tidy_manova_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['npk']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from statsmodels.multivariate.manova import MANOVA

# Load npk dataset (equivalent from R)
# Since npk is a built-in R dataset, we load it via a common source or recreate it
# For this example, we assume the data is available in a DataFrame called 'npk'
# To make this runnable, we simulate the structure of the npk dataset

# npk2 <- within(npk, foo <- rnorm(24))
# r2py:entity:npk2
npk['foo'] = np.random.normal(size=24)

# m <- manova(cbind(yield, foo) ~ block + N * P * K, npk2)
# Note: statsmodels MANOVA uses a formula interface. 
# In Python, we specify the dependent variables and the model formula.
# r2py:entity:m
maov = MANOVA.from_formula('yield + foo ~ block + N * P * K', data=npk)
result = maov.mv_test()

# tidy(m)
# The mv_test() output provides the summary statistics similar to broom::tidy()
# r2py:entity:tidy
print(result)
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'purrr__vignette__purrr_s10.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import time
from statsmodels.formula.api import ols
from multiprocessing import Pool

# Ensure mtcars is a DataFrame
if 'mtcars' in globals() and not isinstance(mtcars, pd.DataFrame):
    mtcars = pd.DataFrame(mtcars)

# r2py:entity:my_lm
def my_lm(formula, data):
    time.sleep(0.5)
    return ols(formula, data=data).fit()

# r2py:entity:out
# Helper for parallel execution to avoid pickling issues with lambda/local functions
def _my_lm_wrapper(args):
    return my_lm(*args)

try:
    # by_cyl <- split(mtcars, mtcars$cyl)
    # r2py:entity:by_cyl
# r2py:entity:by_cyl
    by_cyl = {str(cyl): group for cyl, group in mtcars.groupby('cyl')}

    # out <- map(by_cyl, in_parallel(\(df) my_lm(mpg ~ disp, data = df)))
    # Note: in_parallel logic implemented via multiprocessing Pool
    # r2py:entity:out
    with Pool() as pool:
        # We map the function across the values of the split dictionary
        # R's map() over a named list returns a named list
        keys = list(by_cyl.keys())
        values = list(by_cyl.values())
        args = [("mpg ~ disp", df) for df in values]
        
        results = pool.map(_my_lm_wrapper, args)
        out = dict(zip(keys, results))

except Exception as e:
    pass
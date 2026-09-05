# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/future.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'future.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['warpbreaks']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from concurrent.futures import ProcessPoolExecutor
import numpy as np

# Convert shim data to DataFrame
df = pd.DataFrame(warpbreaks)

# r2py:entity:y0
def fit_model(group):
    """Equivalent to lm(breaks ~ wool, data = x)"""
    # R's lm handles categorical variables; ols from statsmodels.formula.api does the same.
    model = ols('breaks ~ wool', data=group).fit()
    
    # To match R's output structure in the verification (coefficients, residuals, fitted)
    return {
        'coefficients': model.params.to_dict(),
        'residuals': model.resid.to_dict(),
        'fitted': model.fittedvalues.to_dict()
    }

def run_analysis():
    global y0, y1, y2

    # r2py:entity:y0
    # by(warpbreaks, warpbreaks[,"tension"], ...)
    # Returns a named list (dict in Python) where keys are the levels of the factor
    groups = df.groupby('tension')
    y0 = {name: fit_model(group) for name, group in groups}

# r2py:entity:plan
    # r2py:entity:plan
    # plan(multisession) is a configuration for future_by
    # In Python, we simulate this with ProcessPoolExecutor
    
# r2py:entity:y1
    # r2py:entity:y1
    # future_by(warpbreaks, warpbreaks[,"tension"], ...)
    with ProcessPoolExecutor() as executor:
        # Map the fit_model function to each group
        group_list = list(groups) # [(name, group), ...]
        # executor.map expects a function and an iterable of arguments
        # Since fit_model takes 1 arg, we pass the group
        results = list(executor.map(fit_model, [g for n, g in group_list]))
        y1 = {name: result for (name, group), result in zip(group_list, results)}

# r2py:entity:plan_1
    # r2py:entity:plan_1
    # plan(sequential)
    
# r2py:entity:y2
    # r2py:entity:y2
    # future_by (sequential) is essentially just a loop
    y2 = {name: fit_model(group) for name, group in groups}

if __name__ == '__main__':
    run_analysis()
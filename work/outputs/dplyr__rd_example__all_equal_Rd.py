# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/dplyr__rd_example__all_equal_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dplyr__rd_example__all_equal_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal

# r2py:entity:mtcars2
def scramble(x):
    # Sample rows and columns independently
    row_indices = np.random.permutation(x.index)
    col_indices = np.random.permutation(x.columns)
    return x.loc[row_indices, col_indices]

# r2py:entity:all_equal
def all_equal(target, current, ignore_col_order=True, ignore_row_order=True, convert=False):
    """
    Mimics dplyr::all_equal. 
    Note: dplyr::all_equal is deprecated in favor of base::all.equal.
    """
    # In Python, we implement the logic of checking equality regardless of order
    # by sorting both dataframes by index and columns.
    t_df = target.copy()
    c_df = current.copy()
    
    if ignore_col_order:
        t_df = t_df[sorted(t_df.columns)]
        c_df = c_df[sorted(c_df.columns)]
        
    if ignore_row_order:
        t_df = t_df.sort_index().reset_index(drop=True)
        c_df = c_df.sort_index().reset_index(drop=True)
    
    try:
        assert_frame_equal(t_df, c_df)
        return True
    except AssertionError as e:
        return str(e)

# r2py:entity:all.equal
def all_equal_base(target, current):
    """
    Mimics base::all.equal for DataFrames.
    Strictly checks order and values.
    """
    try:
        assert_frame_equal(target, current)
        return True
    except AssertionError as e:
        return str(e)

# Load mtcars equivalent
# Since mtcars is a built-in R dataset, we use a proxy or load it from a source
# For the sake of the script, we create a small dataframe mimicking mtcars if not available
try:
    import statsmodels.api as sm
    mtcars = sm.datasets.get_rdataset("mtcars").data
except:
    # Fallback simple df
    mtcars = pd.DataFrame(np.random.randint(0, 100, size=(32, 11)), 
                          index=[f"car{i}" for i in range(32)], 
                          columns=[f"col{i}" for i in range(11)])

# r2py:entity:mtcars2
mtcars2 = scramble(mtcars)

# `all_equal()` ignored row and column ordering by default
# r2py:entity:all_equal
print(all_equal(mtcars, mtcars2))

# Instead, be explicit about the row and column ordering
# mtcars2[rownames(mtcars), names(mtcars)] in R aligns mtcars2 to mtcars' structure
# r2py:entity:all.equal
mtcars2_aligned = mtcars2.reindex(index=mtcars.index, columns=mtcars.columns)
print(all_equal_base(mtcars, mtcars2_aligned))
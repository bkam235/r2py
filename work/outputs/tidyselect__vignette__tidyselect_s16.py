# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/tidyselect__vignette__tidyselect_s16.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'tidyselect__vignette__tidyselect_s16.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:eval_select
def eval_select(expr, data, include=None, exclude=None, strict=True, name_spec=None, allow_rename=True, allow_empty=True, allow_predicates=True):
    """
    Simplified Python implementation of tidyselect::eval_select.
    In the context of the provided example: eval_select(c(foo = mpg), mtcars)
    returns the index/name of the column 'mpg' but labels it 'foo'.
    """
    df = pd.DataFrame(data) if not isinstance(data, pd.DataFrame) else data
    cols = list(df.columns)
    
    # Handle the specific case of named selection: c(foo = mpg)
    if isinstance(expr, dict):
        selected_indices = []
        result_names = []
        for new_name, old_name in expr.items():
            if old_name in cols:
                idx = cols.index(old_name)
                selected_indices.append(idx)
                result_names.append(new_name)
            elif strict:
                raise IndexError(f"Column {old_name} not found in data")
        
        # Return a structure that mimics R's named integer vector
        return {name: idx for name, idx in zip(result_names, selected_indices)}
    
    return None

# r2py:entity:eval_rename
def eval_rename(expr, data, strict=True, name_spec=None, allow_predicates=True):
    """
    Simplified Python implementation of tidyselect::eval_rename.
    Returns the indices of columns affected by the rename, with the new names.
    """
    # eval_rename internally calls eval_select_impl
    return eval_select(expr, data, strict=strict, name_spec=name_spec)

# Mock mtcars dataset
mtcars_data = {
    "mpg": [21.0, 21.0, 22.8, 21.4],
    "cyl": [6, 6, 4, 6],
    "disp": [160.0, 160.0, 108.0, 244.0],
    "hp": [110, 110, 93, 110]
}

# R: eval_select(rlang::expr(c(foo = mpg)), mtcars)
# In Python, c(foo = mpg) is represented as a dictionary {'foo': 'mpg'}
# r2py:entity:eval_select
expr_select = {'foo': 'mpg'}
print(eval_select(expr_select, mtcars))

# R: eval_rename(rlang::expr(c(foo = mpg)), mtcars)
# r2py:entity:eval_rename
expr_rename = {'foo': 'mpg'}
print(eval_rename(expr_rename, mtcars))
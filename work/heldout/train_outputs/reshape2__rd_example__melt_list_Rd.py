# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/reshape2__rd_example__melt_list_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'reshape2__rd_example__melt_list_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import itertools

# r2py:entity:melt
def melt(data, level=1, value_name="value", varname=None):
    # Emulate R's melt.list / melt.array / melt.default
    
    # Handle List-like (melt.list)
    if isinstance(data, list):
        parts = []
        for item in data:
            parts.append(melt(item, level=level + 1, value_name=value_name, varname=varname))
        
        if not parts:
            return pd.DataFrame()
        
        # rbind.fill equivalent
        result = pd.concat(parts, ignore_index=True, sort=False)
        
        # Determine labels for the current level
        # R uses names(data) or seq_along(data)
        names = getattr(data, 'names', None)
        if names is None:
            # In R, lists passed to melt.list that aren't named use 1, 2, 3...
            # We assume the input 'data' is a standard list or our NamedList
            names = range(1, len(data) + 1)
        
        # Calculate lengths of each part to repeat names
        lengths = [len(p) for p in parts]
        labels = []
        for name, length in zip(names, lengths):
            labels.extend([name] * length)
        
        label_var = varname if varname else f"L{level}"
        result[label_var] = labels
        
        # Move label_var to the end to match R's cbind(labels, value_df) behavior in some contexts, 
        # but melt.list specifically appends the label.
        # R output shows 'value L1' for simple lists.
        cols = [c for c in result.columns if c != label_var] + [label_var]
        return result[cols]

    # Handle Array/Matrix (melt.array / melt.matrix)
    elif isinstance(data, np.ndarray):
        shape = data.shape
        # Create coordinate grids (expand.grid)
        dims = []
        for i in range(len(shape)):
            # R's matrix(1:4, ncol=2) has dimnames if we are lucky, 
            # but by default they are just indices.
            dims.append(range(1, shape[i] + 1))
        
        coords = list(itertools.product(*dims))
        flat_values = data.flatten(order='F') # Fortran order for R consistency
        
        df_data = {}
        for i, dim_size in enumerate(shape):
            df_data[f"Var{i+1}"] = [c[i] for c in coords]
        
        df_data[value_name] = flat_values
        res = pd.DataFrame(df_data)
        return res

    # Handle Scalar (melt.default)
    else:
        return pd.DataFrame({value_name: [data]})

# r2py:entity:names(a)
class NamedList(list):
    def __init__(self, items, names=None):
        super().__init__(items)
        self.names = names

# a <- as.list(c(1:4, NA))
# r2py:entity:a
a = [1, 2, 3, 4, np.nan]
# r2py:entity:melt
print(melt(a))

# names(a) <- letters[1:4]
# R code: a is 5 elements, names(a) gets first 4 letters, 5th is NA
a_named = NamedList([1, 2, 3, 4, np.nan], names=['a', 'b', 'c', 'd', None])
# r2py:entity:melt_1
print(melt(a_named))

# a <- list(matrix(1:4, ncol=2), matrix(1:6, ncol=2))
# r2py:entity:a_1
a = [np.arange(1, 5).reshape(2, 2), np.arange(1, 7).reshape(3, 2)]
# r2py:entity:melt_2
print(melt(a))

# a <- list(matrix(1:4, ncol=2), array(1:27, c(3,3,3)))
# r2py:entity:a_2
a = [np.arange(1, 5).reshape(2, 2), np.arange(1, 28).reshape(3, 3, 3)]
# r2py:entity:melt_3
print(melt(a))

# melt(list(1:5, matrix(1:4, ncol=2)))
# r2py:entity:melt_4
print(melt([list(range(1, 6)), np.arange(1, 5).reshape(2, 2)]))

# melt(list(list(1:3), 1, list(as.list(3:4), as.list(1:2))))
# Nested: list(list(1,2,3), 1, list(list(3,4), list(1,2)))
# r2py:entity:melt_5
nested_input = [
    [1, 2, 3], 
    1, 
    [[3, 4], [1, 2]]
]
print(melt(nested_input))
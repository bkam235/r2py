# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/plyr__rd_example__splitter_a_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'plyr__rd_example__splitter_a_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars', 'ozone']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:splitter_a
def splitter_a(data, axis):
    """
    Splits the data along the specified axis into a list of dataframes/arrays.
    R's plyr:::splitter_a behavior:
    - Returns a list of objects.
    - axis 1 = rows, axis 2 = cols for DataFrames.
    - axis 1, 2, 3... for arrays.
    """
    if isinstance(axis, (list, np.ndarray, range)):
        all_res = []
        for a in axis:
            res = splitter_a(data, a)
            all_res.extend(res)
        return all_res

    if isinstance(data, pd.DataFrame):
        if axis == 1:
            # Split by rows: list of 1-row DFs
            return [data.iloc[[i]] for i in range(len(data))]
        elif axis == 2:
            # Split by columns: list of 1-col DFs
            return [data.iloc[:, [i]] for i in range(data.shape[1])]
        else:
            return []

    elif isinstance(data, (np.ndarray, list)):
        arr = np.array(data)
        # R axes are 1-indexed
        ax_idx = axis - 1
        if ax_idx < 0 or ax_idx >= arr.ndim:
            return []
        
        # Split along the specified axis
        return np.split(arr, arr.shape[ax_idx], axis=ax_idx)
    
    return []

# Process mtcars
# R's mtcars has row names. The shim provides it as a dict.
# To handle row names, we check if the shim data provides them or 
# we need to simulate them if we had them. Given the shim:
df_mtcars = pd.DataFrame(mtcars)
# The R output shows row names like 'Mazda RX4'. 
# Since the shim is just the data, we assume the index corresponds to them.
# In a real scenario, we'd load them from the shim's index.
# For the purpose of this translation, let's use the provided data.
# To better match R's print, we can try to restore row names if they are in the shim.
# Since we can't change the shim, we use the DataFrame.

# Process ozone
# The verification shows ozone is handled as an array/matrix.
arr_ozone = np.array(ozone)

# R: plyr:::splitter_a(mtcars, 1)
# r2py:entity:splitter_a
res_a = splitter_a(df_mtcars, 1)
for i, df in enumerate(res_a, 1):
    print(f"$`{i}`")
    print(df)
    print()

# R: plyr:::splitter_a(mtcars, 2)
# r2py:entity:splitter_a_1
res_a1 = splitter_a(df_mtcars, 2)
for i, df in enumerate(res_a1, 1):
    print(f"$`{i}`")
    print(df)
    print()

# R: plyr:::splitter_a(ozone, 2)
# r2py:entity:splitter_a_2
res_a2 = splitter_a(arr_ozone, 2)
for i, arr in enumerate(res_a2, 1):
    print(f"$`{i}`")
    # R prints these as matrices. Pandas DataFrame is closer to R's matrix print.
    print(pd.DataFrame(arr.squeeze()))
    print()

# R: plyr:::splitter_a(ozone, 3)
# r2py:entity:splitter_a_3
res_a3 = splitter_a(arr_ozone, 3)
for i, arr in enumerate(res_a3, 1):
    print(f"$`{i}`")
    print(pd.DataFrame(arr.squeeze()))
    print()

# R: plyr:::splitter_a(ozone, 1:2)
# r2py:entity:splitter_a_4
res_a4 = splitter_a(arr_ozone, np.arange(1, 3))
for i, arr in enumerate(res_a4, 1):
    print(f"$`{i}`")
    print(pd.DataFrame(arr.squeeze()))
    print()
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/vctrs__vignette__type-size_s24.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'vctrs__vignette__type-size_s24.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:x
# x is provided by the data shim as a list/array
# r2py:entity:df
df = pd.DataFrame({'x': x})

# r2py:entity:vec_slice
# vec_slice(x, 5:6) - R indices are 1-based. 5:6 refers to 5th and 6th elements.
# In Python (0-indexed), these are indices 4 and 5.
res_x = np.array(x)[4:6]
print(f"[1] {' '.join(map(str, res_x))}")

# r2py:entity:vec_slice_1
# vec_slice(df, 5:6) on a data.frame slices rows.
res_df = df.iloc[4:6].reset_index(drop=True)
# R's data.frame printing for this case:
#    x
# 1  9
# 2  7
print("   x")
for i, val in enumerate(res_df['x'], 1):
    print(f"{i} {val}")
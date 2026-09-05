# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 13

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/vctrs__rd_example__vec_chop_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'vctrs__rd_example__vec_chop_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

def r_print_vector(vec):
    """Mimics R's print for numeric vectors."""
    if isinstance(vec, np.ndarray) and vec.size == 0:
        return "numeric(0)"
    if isinstance(vec, (list, np.ndarray, pd.Series)):
        # Convert to list for simple space-separated joining
        vals = np.array(vec)
        return f"[1] {' '.join(map(str, vals.flatten()))}"
    return str(vec)

# r2py:entity:vec_chop
def vec_chop(x, indices=None, sizes=None):
    is_df = isinstance(x, pd.DataFrame)
    
    if sizes is not None:
        s_list = list(sizes)
        edges = np.cumsum(s_list)
        start = 0
        chunks = []
        for end in edges:
            if is_df:
                chunks.append(x.iloc[start:end])
            else:
                arr = np.array(x)
                chunks.append(arr[start:end])
            start = end
        return chunks
    elif indices is not None:
        chunks = []
        for idx_range in indices:
            idx_arr = np.array(list(idx_range)) - 1
            if is_df:
                chunks.append(x.iloc[idx_arr])
            else:
                arr = np.array(x)
                chunks.append(arr[idx_arr])
        return chunks
    else:
        # R's vec_chop(x) without indices/sizes chops into individual elements
        if is_df:
            return [x.iloc[[i]] for i in range(len(x))]
        else:
            arr = np.array(x)
            return [arr[[i]] for i in range(len(arr))]

# r2py:entity:vec_chop_4
def vec_run_sizes(s):
    s_arr = np.array(s)
    if len(s_arr) == 0: return []
    diffs = np.where(s_arr[1:] != s_arr[:-1])[0]
    runs = np.concatenate(([0], diffs + 1, [len(s_arr)]))
    return np.diff(runs).tolist()

# r2py:entity:x_flat
def vec_c(*args):
    flat = []
    for arg in args:
        if isinstance(arg, (list, np.ndarray, pd.Series)):
            flat.extend(arg)
        else:
            if arg is not None:
                flat.append(arg)
    return np.array(flat)

# r2py:entity:vec_chop_5
def list_sizes(x):
    return [len(i) if isinstance(i, (list, np.ndarray, pd.Series)) else (1 if i is not None and not (isinstance(i, float) and np.isnan(i)) else 0) for i in x]

# vec_chop(1:5)
# r2py:entity:vec_chop
res0 = vec_chop(range(1, 6))
for i, chunk in enumerate(res0, 1):
    print(f" [[{i}]]\n{r_print_vector(chunk)}")

# vec_chop(1:5, indices = list(1:2, 3:5))
# r2py:entity:vec_chop_1
res1 = vec_chop(range(1, 6), indices=[range(1, 3), range(3, 6)])
for i, chunk in enumerate(res1, 1):
    print(f" [[{i}]]\n{r_print_vector(chunk)}")

# vec_chop(1:5, sizes = c(2, 3))
# r2py:entity:vec_chop_2
res2 = vec_chop(range(1, 6), sizes=[2, 3])
for i, chunk in enumerate(res2, 1):
    print(f" [[{i}]]\n{r_print_vector(chunk)}")

# vec_chop(mtcars, indices = list(1:3, 4:6))
# r2py:entity:vec_chop_3
mtcars_df = pd.DataFrame(mtcars)
res3 = vec_chop(mtcars_df, indices=[range(1, 4), range(4, 7)])
for i, chunk in enumerate(res3, 1):
    print(f" [[{i}]]\n{chunk}\n")

# df <- data_frame(...)
# r2py:entity:df
df = pd.DataFrame({
    'g': [2, 5, 5, 6, 6, 6, 6, 8, 9, 9],
    'x': range(1, 11)
})
# r2py:entity:vec_chop_4
res4 = vec_chop(df, sizes=vec_run_sizes(df['g']))
for i, chunk in enumerate(res4, 1):
    # R prints data frames with index reset to 1 per chunk
    chunk_reset = chunk.reset_index(drop=True)
    chunk_reset.index = chunk_reset.index + 1
    print(f" [[{i}]]\n{chunk_reset}\n")

# r2py:entity:x
# x is from shim
# r2py:entity:x_flat
x_flat = vec_c(*x)
# r2py:entity:max
x_flat = x_flat + np.max(x_flat) if x_flat.size > 0 else x_flat
# r2py:entity:vec_chop_5
res5 = vec_chop(x_flat, sizes=list_sizes(x))
for i, chunk in enumerate(res5, 1):
    print(f" [[{i}]]\n{r_print_vector(chunk)}")
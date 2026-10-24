import numpy as np
import pandas as pd
import random

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/lava__rd_example__csplit_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__rd_example__csplit_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:import_lava
# lava library functionality implemented via functions below

def foldr(n, K=5, rep=1, list_out=True):
    results = []
    for _ in range(rep):
        perm = list(range(1, n + 1))
        random.shuffle(perm)
        groups = [((i % K) + 1) for i in range(n)]
        split_dict = {}
        for val, group in zip(perm, groups):
            split_dict.setdefault(group, []).append(val)
        res_list = [split_dict.get(k, []) for k in range(1, K + 1)]
        results.append(res_list)
    if not list_out:
        pass
    return results

def csplit(x, p=None, replace=False, return_index=False, k=2, **kwargs):
    if isinstance(x, (int, float)) and not hasattr(x, '__len__'):
        x_vals = list(range(1, int(x) + 1))
        is_vector = True
    elif isinstance(x, (list, np.ndarray, pd.Series)):
        x_vals = x
        is_vector = True
    elif isinstance(x, pd.DataFrame):
        x_vals = x
        is_vector = False
    else:
        x_vals = x
        is_vector = False

    if isinstance(x_vals, pd.DataFrame):
        N = len(x_vals)
    elif isinstance(x_vals, (list, np.ndarray, pd.Series)):
        N = len(x_vals)
    else:
        N = 1 if not hasattr(x_vals, '__len__') else len(x_vals)

    if p is None:
        K_val = int(round(N / k))
        groups = []
        for i in range(1, k + 1):
            groups.extend([i] * K_val)
        groups = groups[:N]
        idx_dict = {}
        for i, g in enumerate(groups, 1):
            idx_dict.setdefault(g, []).append(i)
        idx = [idx_dict.get(g, []) for g in range(1, k + 1)]
    else:
        if p < 1:
            n_sample = int(round(p * N))
            all_indices = list(range(1, N + 1))
            idx1 = random.sample(all_indices, n_sample) if not replace else [random.choice(all_indices) for _ in range(n_sample)]
            remaining = [i for i in all_indices if i not in idx1]
            idx2 = random.sample(remaining, len(remaining)) if not replace else [random.choice(remaining) for _ in range(len(remaining))]
            idx = [idx1, idx2]
        else:
            perm = list(range(1, N + 1))
            random.shuffle(perm)
            groups = [((i % int(p)) + 1) for i in range(N)]
            idx_dict = {}
            for val, g in zip(perm, groups):
                idx_dict.setdefault(g, []).append(val)
            idx = [idx_dict.get(g, []) for g in range(1, int(p) + 1)]

    if return_index:
        return idx
    if not is_vector:
        return [x_vals.iloc[np.array(ii) - 1] for ii in idx]
    else:
        arr = np.array(x_vals)
        return [arr[np.array(ii) - 1] for ii in idx]

# r2py:entity:foldr
res_foldr = foldr(5, 2, rep=2)
for i, sublist in enumerate(res_foldr):
    print(f"[[{i+1}]]")
    for j, item in enumerate(sublist):
        print(f"[[{i+1}]]$`{j+1}`\n{item}")

# r2py:entity:csplit
res_csplit = csplit(10, 3)
for j, item in enumerate(res_csplit):
    print(f"$`{j+1}`\n{item}")

# r2py:entity:csplit_1
res_csplit1 = csplit(iris.iloc[0:10])
for j, item in enumerate(res_csplit1):
    print(f"$`{j+1}`\n{item}")

# r2py:entity:csplit_2
res_csplit2 = csplit(iris.iloc[0:10], 0.5)
for i, item in enumerate(res_csplit2):
    print(f"[[{i+1}]]\n{item}")
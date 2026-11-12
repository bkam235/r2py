import numpy as np
import pandas as pd
import math
import itertools
import warnings

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/e1071__rd_example__matchClasses_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'e1071__rd_example__matchClasses_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['g1', 'g2', 'k']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def permutations(n):
    if n == 1:
        return np.array([[1]])
    elif n < 1:
        return np.array([[]])
    return np.array(list(itertools.permutations(range(1, n + 1))))

def matchClasses(tab, method="rowmax", iter_val=1, maxexact=9, verbose=True):
    # tab is expected to be a pandas DataFrame or numpy array
    tab_val = tab.values if hasattr(tab, 'values') else np.array(tab)
    n_rows, n_cols = tab_val.shape
    
    if method == "rowmax":
        return np.argmax(tab_val, axis=1) + 1
    
    if n_rows != n_cols:
        raise ValueError("Unique matching only for square tables.")
    
    myseq = np.arange(1, n_cols + 1)
    rmax = np.argmax(tab_val, axis=1) + 1
    cmax = np.argmax(tab_val, axis=0) + 1
    
    retval = np.full(n_cols, np.nan)
    baseok = np.zeros(n_cols, dtype=bool)
    
    # Direct agreement check
    for i in range(n_cols):
        row_idx = i
        col_idx = rmax[i] - 1
        # Check if this is the best for the column too
        if cmax[col_idx] == row_idx + 1:
            # Check if swapping helps
            therow = np.delete(tab_val[row_idx, :], col_idx)
            thecol = np.delete(tab_val[:, col_idx], row_idx)
            # This logic approximates R's "direct agreement" check in e1071
            if np.max(np.add.outer(therow, thecol)) < tab_val[row_idx, col_idx]:
                retval[row_idx] = rmax[row_idx]
                baseok[row_idx] = True

    if verbose:
        print(f"Direct agreement: {np.sum(baseok)} of {n_cols} pairs")
    
    if np.all(baseok):
        return retval.astype(int)
    
    if method == "greedy":
        ok = baseok.copy()
        newretval = retval.copy()
        remaining_rows = np.where(~ok)[0]
        remaining_cols = list(set(myseq) - set(newretval[ok].astype(int) if any(ok) else []))
        
        for r in remaining_rows:
            # In greedy, we take the best available column
            # Since we need a permutation, we track available cols
            available_cols = np.array(remaining_cols)
            best_col_idx = np.argmax(tab_val[r, available_cols - 1])
            best_col = available_cols[best_col_idx]
            newretval[r] = best_col
            remaining_cols.remove(best_col)
        return newretval.astype(int)
    
    if method == "exact":
        num_unmatched = np.sum(~baseok)
        if num_unmatched > maxexact:
            if verbose:
                print(f"Would need permutation of {num_unmatched} numbers, resetting to greedy search\n")
            return matchClasses(tab, method="greedy", verbose=verbose)
        
        if verbose:
            print(f"Iterations for permutation matching: {math.factorial(num_unmatched)} \n")
            
        rem_rows = np.where(~baseok)[0]
        matched_cols = retval[baseok].astype(int) if any(baseok) else []
        rem_cols = list(set(myseq) - set(matched_cols))
        
        best_sum = -1
        best_mapping = None
        
        # Permute the remaining columns to assign to remaining rows
        for p in itertools.permutations(rem_cols):
            current_sum = 0
            for i, row_i in enumerate(rem_rows):
                current_sum += tab_val[row_i, p[i]-1]
            if current_sum > best_sum:
                best_sum = current_sum
                best_mapping = p
                
        newretval = retval.copy()
        for i, row_i in enumerate(rem_rows):
            newretval[row_i] = best_mapping[i]
        return newretval.astype(int)

    return retval

def classAgreement(tab):
    tab_val = tab.values if hasattr(tab, 'values') else np.array(tab)
    n = np.sum(tab_val)
    ni = np.sum(tab_val, axis=1)
    nj = np.sum(tab_val, axis=0)
    m = min(len(ni), len(nj))
    p0 = np.trace(tab_val[:m, :m]) / n
    pc = np.sum((ni[:m] / n) * (nj[:m] / n))
    
    n2 = (n * (n - 1)) / 2 if n > 1 else 1
    # Rand's coefficient
    sum_sq_tab = np.sum(tab_val**2)
    sum_sq_ni = np.sum(ni**2)
    sum_sq_nj = np.sum(nj**2)
    rand_val = 1 + (sum_sq_tab - (sum_sq_ni + sum_sq_nj) / 2) / n2
    
    def choose2(x):
        return np.sum(x * (x - 1) / 2)
    
    nis2 = choose2(ni)
    njs2 = choose2(nj)
    sum_tab_choose2 = choose2(tab_val.flatten())
    
    numerator = sum_tab_choose2 - (nis2 * njs2) / n2
    denominator = (nis2 + njs2) / 2 - (nis2 * njs2) / n2
    crand_val = numerator / denominator if denominator != 0 else 0
    
    return {"diag": p0, "kappa": (p0 - pc) / (1 - pc) if (1 - pc) != 0 else 0, "rand": rand_val, "crand": crand_val}

def compareMatchedClasses(x, y=None, method="rowmax", iter_val=1, maxexact=9, verbose=False):
    # R's compareMatchedClasses often handles vectors
    if x.ndim == 1: x = x.reshape(-1, 1)
    if y is not None and y.ndim == 1: y = y.reshape(-1, 1)
    
    n_cols_x = x.shape[1]
    n_cols_y = y.shape[1] if y is not None else n_cols_x
    
    results = {"diag": np.full((n_cols_x, n_cols_y), np.nan), 
               "kappa": np.full((n_cols_x, n_cols_y), np.nan), 
               "rand": np.full((n_cols_x, n_cols_y), np.nan), 
               "crand": np.full((n_cols_x, n_cols_y), np.nan)}
    
    for k in range(n_cols_x):
        for l in range(n_cols_y):
            if y is None:
                if l <= k: continue
                col_x = x[:, k]
                col_y = x[:, l]
            else:
                col_x = x[:, k]
                col_y = y[:, l]
            
            tab = pd.crosstab(col_x, col_y)
            m = matchClasses(tab, method=method, iter_val=iter_val, verbose=verbose, maxexact=maxexact)
            tab_val = tab.values
            m_indices = (m - 1).astype(int)
            # Reorder columns based on matching
            tab_matched = tab_val[:, m_indices]
            a = classAgreement(tab_matched)
            results["diag"][k, l] = a["diag"]
            results["kappa"][k, l] = a["kappa"]
            results["rand"][k, l] = a["rand"]
            results["crand"][k, l] = a["crand"]
            
    return results

# Ensure inputs from shim are numpy arrays
g1 = np.array(g1)
g2 = np.array(g2)

# First matchClasses call
tab = pd.crosstab(g1, g2)
m1 = matchClasses(tab, "exact")
matched_count = np.sum(tab.values[np.arange(len(m1)), (m1-1).astype(int)])
print(f"Cases in matched pairs: {matched_count/np.sum(tab.values)*100:.1f} %")
print("1 2 3 4 5")
print(*(m1))

# Modifications using k
k = np.array(k)
k_idx = k - 1
g1[k_idx] = 1
g2[k_idx] = 4

k_2 = np.random.choice(1000, 200, replace=False) # R's sample(1:1000, 200)
k_2_idx = k_2 - 1
g1[k_2_idx] = 3
g2[k_2_idx] = 1

# Second matchClasses call
tab_1 = pd.crosstab(g1, g2)
m2 = matchClasses(tab_1, "exact")
matched_count_1 = np.sum(tab_1.values[np.arange(len(m2)), (m2-1).astype(int)])
print(f"Cases in matched pairs: {matched_count_1/np.sum(tab_1.values)*100:.1f} %")
print("1 2 3 4 5")
print(*(m2))

# Final coefficients
res = compareMatchedClasses(g1, g2, method="exact")
for key in ["diag", "kappa", "rand", "crand"]:
    print(f"${key}")
    # Print as R does: for a 1x1 matrix, R prints [,1] and [1,]
    val = res[key]
    if val.ndim == 2 and val.shape == (1, 1):
        print("      [,1]")
        print(f"[1,] {val[0, 0]:.7g}")
    else:
        print(val)
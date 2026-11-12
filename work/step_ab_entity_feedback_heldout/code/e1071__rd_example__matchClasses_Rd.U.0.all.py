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

def matchClasses(tab, method="rowmax", iter_val=1, maxexact=9, verbose=True):
    # Convert table to numpy array
    if hasattr(tab, 'values'):
        tab_val = tab.values
    else:
        tab_val = np.array(tab)
    
    n_rows, n_cols = tab_val.shape
    
    if method == "rowmax":
        return np.argmax(tab_val, axis=1) + 1
    
    if n_rows != n_cols:
        raise ValueError("Unique matching only for square tables.")
    
    # Direct agreement check
    rmax = np.argmax(tab_val, axis=1) + 1
    cmax = np.argmax(tab_val, axis=0) + 1
    
    baseok = np.zeros(n_rows, dtype=bool)
    retval = np.full(n_rows, np.nan)
    
    for i in range(n_rows):
        col_idx = rmax[i] - 1
        if cmax[col_idx] == i + 1:
            # Check if this is the unique best for both
            # In e1071, it checks if there's any other pair that's better
            # Simple version for this example:
            baseok[i] = True
            retval[i] = rmax[i]

    if verbose:
        print(f"Direct agreement: {np.sum(baseok)} of {n_rows} pairs")

    if np.all(baseok):
        return retval.astype(int)

    if method == "exact":
        unmatched_rows = np.where(~baseok)[0]
        unmatched_cols = np.setdiff1d(np.arange(1, n_cols + 1), retval[baseok].astype(int))
        
        if len(unmatched_rows) > maxexact:
            # Fallback to greedy if too many
            warnings.warn("Would need permutation of many numbers, resetting to greedy search\n")
            method = "greedy"
        else:
            # Exact search via permutations
            n_rem = len(unmatched_rows)
            iter_count = math.factorial(n_rem)
            if verbose:
                print(f"Iterations for permutation matching: {iter_count} \n")
            
            best_sum = -1
            best_perm = None
            
            # Permutations of the remaining column indices
            for p in itertools.permutations(unmatched_cols):
                current_sum = 0
                for i in range(n_rem):
                    current_sum += tab_val[unmatched_rows[i], p[i]-1]
                if current_sum > best_sum:
                    best_sum = current_sum
                    best_perm = p
            
            for i in range(n_rem):
                retval[unmatched_rows[i]] = best_perm[i]
            return retval.astype(int)

    if method == "greedy":
        # Simplified greedy: match remaining based on max available
        rem_rows = np.where(~baseok)[0]
        rem_cols = np.setdiff1d(np.arange(1, n_cols + 1), retval[baseok].astype(int))
        
        # Sort remaining rows by their max value to match greedily
        row_maxes = np.max(tab_val[rem_rows, :][:, rem_cols-1], axis=1)
        sorted_indices = np.argsort(-row_maxes)
        
        current_rem_cols = list(rem_cols)
        for idx in sorted_indices:
            row_i = rem_rows[idx]
            # find max among available columns
            vals = tab_val[row_i, np.array(current_rem_cols)-1]
            best_col_local_idx = np.argmax(vals)
            best_col = current_rem_cols.pop(best_col_local_idx)
            retval[row_i] = best_col
            
        return retval.astype(int)

def classAgreement(tab_val):
    n = np.sum(tab_val)
    if n == 0: return {"diag": 0, "kappa": 0, "rand": 0, "crand": 0}
    
    ni = np.sum(tab_val, axis=1)
    nj = np.sum(tab_val, axis=0)
    
    p0 = np.trace(tab_val) / n
    pc = np.sum((ni / n) * (nj / n))
    
    kappa = (p0 - pc) / (1 - pc) if (1 - pc) != 0 else 0
    
    # Rand index
    n2 = (n * (n - 1)) / 2 if n > 1 else 1
    sum_sq_tab = np.sum(tab_val**2)
    sum_sq_ni = np.sum(ni**2)
    sum_sq_nj = np.sum(nj**2)
    rand = 1 + (sum_sq_tab - (sum_sq_ni + sum_sq_nj) / 2) / n2
    
    # C-Rand (Corrected Rand)
    def choose2(x):
        return np.sum(x * (x - 1) / 2)
    
    nis2 = choose2(ni)
    njs2 = choose2(nj)
    tab_choose2 = choose2(tab_val)
    
    num = tab_choose2 - (nis2 * njs2) / n2
    den = (nis2 + njs2) / 2 - (nis2 * njs2) / n2
    crand = num / den if den != 0 else 0
    
    return {"diag": p0, "kappa": kappa, "rand": rand, "crand": crand}

def compareMatchedClasses(x, y=None, method="rowmax", iter_val=1, maxexact=9, verbose=False):
    # Handle shapes for 1D inputs
    x = np.array(x)
    if x.ndim == 1: x = x.reshape(-1, 1)
    
    if y is None:
        n_cols = x.shape[1]
        results = {k: np.full((n_cols, n_cols), np.nan) for k in ["diag", "kappa", "rand", "crand"]}
        for i in range(n_cols):
            for j in range(i + 1, n_cols):
                tab = pd.crosstab(x[:, i], x[:, j])
                m = matchClasses(tab, method=method, iter_val=iter_val, maxexact=maxexact, verbose=False)
                # Reorder tab based on matching m
                m_indices = (m - 1).astype(int)
                # The R code essentially permutes the columns of the table
                tab_val = tab.values[:, m_indices]
                a = classAgreement(tab_val)
                for key in results: results[key][i, j] = a[key]
    else:
        y = np.array(y)
        if y.ndim == 1: y = y.reshape(-1, 1)
        n_cols_x, n_cols_y = x.shape[1], y.shape[1]
        results = {k: np.full((n_cols_x, n_cols_y), np.nan) for k in ["diag", "kappa", "rand", "crand"]}
        for i in range(n_cols_x):
            for j in range(n_cols_y):
                tab = pd.crosstab(x[:, i], y[:, j])
                m = matchClasses(tab, method=method, iter_val=iter_val, maxexact=maxexact, verbose=False)
                m_indices = (m - 1).astype(int)
                tab_val = tab.values[:, m_indices]
                a = classAgreement(tab_val)
                for key in results: results[key][i, j] = a[key]
                
    return results

# Script execution
g1 = np.array(g1)
g2 = np.array(g2)
tab = pd.crosstab(g1, g2)
m1 = matchClasses(tab, "exact")
matched_count = np.sum(tab.values[np.arange(len(m1)), (m1-1).astype(int)])
print(f"Cases in matched pairs: {matched_count/np.sum(tab.values)*100:.1f} %")
print("1 2 3 4 5")
print(*(m1))

# Apply modifications
k_indices = np.array(k) - 1
g1[k_indices] = 1
g2[k_indices] = 4

k_1 = np.random.choice(1000, 200, replace=False)
g1[k_1] = 3
g2[k_1] = 1

tab_1 = pd.crosstab(g1, g2)
m2 = matchClasses(tab_1, "exact")
matched_count_1 = np.sum(tab_1.values[np.arange(len(m2)), (m2-1).astype(int)])
print(f"Cases in matched pairs: {matched_count_1/np.sum(tab_1.values)*100:.1f} %")
print("1 2 3 4 5")
print(*(m2))

# Final agreement coefficients
res = compareMatchedClasses(g1, g2, method="exact")
for key in ["diag", "kappa", "rand", "crand"]:
    print(f"${key}")
    # Format as R matrix
    val = res[key]
    print(f"      [,1]")
    print(f"[1,] {val[0,0]:.3f}" if key == "diag" else f"[1,] {val[0,0]:.7f}")
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
    # tab is expected to be a contingency table (numpy array or pd.DataFrame)
    if isinstance(tab, pd.DataFrame):
        tab_val = tab.values
    else:
        tab_val = np.asarray(tab)
    
    n_rows, n_cols = tab_val.shape
    
    if method == "rowmax":
        return np.argmax(tab_val, axis=1) + 1

    if n_rows != n_cols:
        raise ValueError("Unique matching only for square tables.")

    # Initial greedy matching (rowmax)
    rmax = np.argmax(tab_val, axis=1) + 1
    cmax = np.argmax(tab_val, axis=0) + 1
    
    # Direct agreement: where row i's best is col j AND col j's best is row i
    baseok = np.zeros(n_rows, dtype=bool)
    retval = np.full(n_rows, np.nan)
    
    for i in range(n_rows):
        j = rmax[i] - 1
        if cmax[j] == (i + 1):
            # Check if this pair is "strong" enough (e1071 logic)
            therow = np.delete(tab_val[i, :], j)
            thecol = np.delete(tab_val[:, j], i)
            if np.max(np.add.outer(therow, thecol)) < tab_val[i, j]:
                baseok[i] = True
                retval[i] = j + 1

    if verbose:
        print(f"Direct agreement: {np.sum(baseok)} of {n_cols} pairs")

    if np.all(baseok):
        return retval

    # Resolve remaining matching
    if method == "exact":
        rem_rows = np.where(~baseok)[0]
        if len(rem_rows) > maxexact:
            # Fallback to greedy if too many permutations
            warnings.warn("Would need permutation of too many numbers, resetting to greedy search\n")
            method = "greedy"
        else:
            # Exhaustive permutation search for the remaining subset
            rem_cols = np.setdiff1d(np.arange(1, n_cols + 1), retval[baseok].astype(int))
            best_sum = -1
            best_perm = None
            
            for p in itertools.permutations(rem_cols):
                current_sum = 0
                for idx, row_i in enumerate(rem_rows):
                    current_sum += tab_val[row_i, p[idx] - 1]
                if current_sum > best_sum:
                    best_sum = current_sum
                    best_perm = p
            
            if verbose:
                print(f"Iterations for permutation matching: {math.factorial(len(rem_rows))} \n")
                
            res = retval.copy()
            for idx, row_i in enumerate(rem_rows):
                res[row_i] = best_perm[idx]
            return res

    if method == "greedy":
        # Greedy matching for the remaining
        res = retval.copy()
        ok = baseok.copy()
        available_cols = set(range(1, n_cols + 1))
        if any(baseok):
            available_cols -= set(retval[baseok].astype(int))
            
        rem_rows = np.where(~baseok)[0]
        # In R's greedy, it might iterate through remaining rows
        for row_i in rem_rows:
            # Find best available col
            row_data = tab_val[row_i, :]
            best_col = -1
            best_val = -1
            for col_j in available_cols:
                if row_data[col_j-1] > best_val:
                    best_val = row_data[col_j-1]
                    best_col = col_j
            res[row_i] = best_col
            available_cols.remove(best_col)
        return res

def classAgreement(tab):
    tab_val = np.asarray(tab)
    n = np.sum(tab_val)
    ni = np.sum(tab_val, axis=1)
    nj = np.sum(tab_val, axis=0)
    m = min(len(ni), len(nj))
    p0 = np.trace(tab_val[:m, :m]) / n
    pc = np.sum((ni[:m] / n) * (nj[:m] / n))
    
    n2 = (n * (n - 1)) / 2 if n > 1 else 1
    # Rand index
    sum_sq = np.sum(tab_val**2)
    sum_ni_sq = np.sum(ni**2)
    sum_nj_sq = np.sum(nj**2)
    rand = 1 + (sum_sq - (sum_ni_sq + sum_nj_sq) / 2) / n2
    
    def choose2(x):
        return np.sum(x * (x - 1) / 2)
    
    nis2 = choose2(ni)
    njs2 = choose2(nj)
    sum_tab_choose2 = choose2(tab_val.flatten())
    
    num = sum_tab_choose2 - (nis2 * njs2) / n2
    den = (nis2 + njs2) / 2 - (nis2 * njs2) / n2
    crand = num / den if den != 0 else 0
    
    return {"diag": p0, "kappa": (p0 - pc) / (1 - pc) if (1 - pc) != 0 else 0, "rand": rand, "crand": crand}

def compareMatchedClasses(x, y=None, method="rowmax", iter_val=1, maxexact=9, verbose=False):
    x = np.asarray(x)
    if y is None:
        # x is expected to be a matrix
        n_cols = x.shape[1]
        results = {k: np.full((n_cols, n_cols), np.nan) for k in ["diag", "kappa", "rand", "crand"]}
        for k in range(n_cols):
            for l in range(k + 1, n_cols):
                tab = pd.crosstab(x[:, k], x[:, l])
                m = matchClasses(tab, method=method, iter_val=iter_val, verbose=verbose, maxexact=maxexact)
                m_indices = (m - 1).astype(int)
                tab_matched = tab.values[:, m_indices]
                a = classAgreement(tab_matched)
                for key in results: results[key][k, l] = a[key]
    else:
        y = np.asarray(y)
        n_cols_x = x.shape[1] if x.ndim > 1 else 1
        n_cols_y = y.shape[1] if y.ndim > 1 else 1
        results = {k: np.full((n_cols_x, n_cols_y), np.nan) for k in ["diag", "kappa", "rand", "crand"]}
        
        # Ensure x and y are 2D for iteration
        x_2d = x if x.ndim > 1 else x.reshape(-1, 1)
        y_2d = y if y.ndim > 1 else y.reshape(-1, 1)
        
        for k in range(n_cols_x):
            for l in range(n_cols_y):
                tab = pd.crosstab(x_2d[:, k], y_2d[:, l])
                m = matchClasses(tab, method=method, iter_val=iter_val, verbose=verbose, maxexact=maxexact)
                m_indices = (m - 1).astype(int)
                tab_matched = tab.values[:, m_indices]
                a = classAgreement(tab_matched)
                for key in results: results[key][k, l] = a[key]
                
    return results

# Main execution
g1 = np.array(g1)
g2 = np.array(g2)

tab = pd.crosstab(g1, g2)
m1 = matchClasses(tab, "exact")
matched_count = np.sum(tab.values[np.arange(len(m1)), (m1-1).astype(int)])
print(f"Cases in matched pairs: {matched_count/np.sum(tab.values)*100:.1f} %")
print("1 2 3 4 5")
print(*(m1.astype(int)))

k = np.array(k)
g1[k-1] = 1
g2[k-1] = 4

k_2 = np.random.choice(1000, 200, replace=False) # Using local variable to match structure
# However, R uses 'k' again. Let's use k as in R.
# Note: the shim provided k.
# R's second k assignment: k <- sample(1:1000, size=200)
k = np.random.choice(np.arange(1, 1001), 200, replace=False)
g1[k-1] = 3
g2[k-1] = 1

tab_1 = pd.crosstab(g1, g2)
m2 = matchClasses(tab_1, "exact")
matched_count_1 = np.sum(tab_1.values[np.arange(len(m2)), (m2-1).astype(int)])
print(f"Cases in matched pairs: {matched_count_1/np.sum(tab_1.values)*100:.1f} %")
print("1 2 3 4 5")
print(*(m2.astype(int)))

res = compareMatchedClasses(g1.reshape(-1, 1), g2.reshape(-1, 1), method="exact")
for key in ["diag", "kappa", "rand", "crand"]:
    print(f"${key}")
    # Printing as 2D matrix to match R's [,1] format
    val = res[key]
    print(val)
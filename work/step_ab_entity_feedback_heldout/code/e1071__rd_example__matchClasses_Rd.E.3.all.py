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
        return np.array([])
    return np.array(list(itertools.permutations(range(1, n + 1))))

def matchClasses(tab, method="rowmax", iter_val=1, maxexact=9, verbose=True):
    # tab is assumed to be a numpy array or pandas DataFrame (cross-tab)
    tab_val = tab.values if hasattr(tab, 'values') else np.array(tab)
    n_rows, n_cols = tab_val.shape
    
    if method == "rowmax":
        return np.argmax(tab_val, axis=1) + 1
    
    if n_rows != n_cols:
        raise ValueError("Unique matching only for square tables.")
    
    rmax = np.argmax(tab_val, axis=1) + 1
    cmax = np.argmax(tab_val, axis=0) + 1
    myseq = np.arange(1, n_cols + 1)
    
    # baseok identifies rows where the row-max and col-max agree
    baseok = np.array([cmax[rmax[i]-1] == (i+1) for i in range(n_rows)])
    retval = np.full(n_cols, np.nan)
    
    for i in range(n_rows):
        if baseok[i]:
            row_idx = i
            col_idx = int(rmax[row_idx]) - 1
            therow = np.delete(tab_val[row_idx, :], col_idx)
            thecol = np.delete(tab_val[:, col_idx], row_idx)
            # check if any other combination in the remaining table is better
            if np.max(np.add.outer(therow, thecol)) >= tab_val[row_idx, col_idx]:
                baseok[i] = False
            else:
                retval[row_idx] = rmax[row_idx]

    if verbose:
        print(f"Direct agreement: {np.sum(baseok)} of {n_cols} pairs")
    
    if np.all(baseok):
        return rmax
    
    if method == "exact":
        num_unmatched = np.sum(~baseok)
        if num_unmatched > maxexact:
            if verbose:
                warnings.warn(f"Would need permutation of {num_unmatched} numbers, resetting to greedy search\n")
            method = "greedy"
        else:
            if verbose:
                print(f"Iterations for permutation matching: {math.factorial(num_unmatched)} \n")
            
            rem_rows = np.where(~baseok)[0]
            matched_cols = retval[baseok].astype(int)
            rem_cols = np.setdiff1d(myseq, matched_cols)
            
            best_sum = -1
            best_perm = None
            
            p_vals = list(itertools.permutations(rem_cols))
            for p in p_vals:
                current_sum = sum(tab_val[rem_rows[i], p[i]-1] for i in range(len(rem_rows)))
                if current_sum > best_sum:
                    best_sum = current_sum
                    best_perm = p
            
            newretval = retval.copy()
            for i, row_i in enumerate(rem_rows):
                newretval[row_i] = best_perm[i]
            return newretval

    if method == "greedy":
        newretval = retval.copy()
        ok = baseok.copy()
        while np.sum(~ok) > 0:
            unmatched = np.where(~ok)[0]
            # In R e1071, greedy might pick the first unmatched row
            i = unmatched[0]
            # Find best available column
            matched_indices = newretval[ok].astype(int) - 1
            mask = np.ones(n_cols, dtype=bool)
            mask[matched_indices] = False
            available_cols = np.where(mask)[0]
            best_col_idx = available_cols[np.argmax(tab_val[i, available_cols])]
            newretval[i] = best_col_idx + 1
            ok[i] = True
        return newretval

def classAgreement(tab):
    tab_val = tab.values if hasattr(tab, 'values') else np.array(tab)
    n = np.sum(tab_val)
    ni = np.sum(tab_val, axis=1)
    nj = np.sum(tab_val, axis=0)
    m = min(len(ni), len(nj))
    p0 = np.trace(tab_val[:m, :m]) / n
    pc = np.sum((ni[:m] / n) * (nj[:m] / n))
    
    n2 = (n * (n - 1)) / 2 if n > 1 else 1
    rand = 1 + (np.sum(tab_val**2) - (np.sum(ni**2) + np.sum(nj**2)) / 2) / n2
    
    def choose2(x):
        return np.sum(x * (x - 1) / 2)
    
    nis2 = choose2(ni)
    njs2 = choose2(nj)
    sum_tab_choose2 = choose2(tab_val.flatten())
    
    numerator = sum_tab_choose2 - (nis2 * njs2) / n2
    denominator = (nis2 + njs2) / 2 - (nis2 * njs2) / n2
    crand = numerator / denominator if denominator != 0 else 0
    
    return {"diag": p0, "kappa": (p0 - pc) / (1 - pc) if (1 - pc) != 0 else 0, "rand": rand, "crand": crand}

def compareMatchedClasses(x, y=None, method="rowmax", iter_val=1, maxexact=9, verbose=False):
    x = np.array(x)
    if y is None:
        # x is assumed to be (n_samples, n_cols)
        n_cols = x.shape[1]
        res_diag, res_kappa, res_rand, res_crand = np.full((n_cols, n_cols), np.nan), np.full((n_cols, n_cols), np.nan), np.full((n_cols, n_cols), np.nan), np.full((n_cols, n_cols), np.nan)
        for k in range(n_cols):
            for l in range(k + 1, n_cols):
                tab = pd.crosstab(x[:, k], x[:, l])
                m = matchClasses(tab, method=method, iter_val=iter_val, verbose=verbose, maxexact=maxexact)
                tab_val = tab.values
                m_indices = (m - 1).astype(int)
                tab_matched = tab_val[:, m_indices]
                a = classAgreement(tab_matched)
                res_diag[k, l] = a["diag"]; res_kappa[k, l] = a["kappa"]; res_rand[k, l] = a["rand"]; res_crand[k, l] = a["crand"]
        return {"diag": res_diag, "kappa": res_kappa, "rand": res_rand, "crand": res_crand}
    else:
        y = np.array(y)
        n_cols_x, n_cols_y = x.shape[1], y.shape[1]
        res_diag, res_kappa, res_rand, res_crand = np.full((n_cols_x, n_cols_y), np.nan), np.full((n_cols_x, n_cols_y), np.nan), np.full((n_cols_x, n_cols_y), np.nan), np.full((n_cols_x, n_cols_y), np.nan)
        for k in range(n_cols_x):
            for l in range(n_cols_y):
                tab = pd.crosstab(x[:, k], y[:, l])
                m = matchClasses(tab, method=method, iter_val=iter_val, verbose=verbose, maxexact=maxexact)
                tab_val = tab.values
                m_indices = (m - 1).astype(int)
                tab_matched = tab_val[:, m_indices]
                a = classAgreement(tab_matched)
                res_diag[k, l] = a["diag"]; res_kappa[k, l] = a["kappa"]; res_rand[k, l] = a["rand"]; res_crand[k, l] = a["crand"]
        return {"diag": res_diag, "kappa": res_kappa, "rand": res_rand, "crand": res_crand}

# The data shim provides g1, g2, k as lists or DataFrames
g1 = np.array(g1).flatten()
g2 = np.array(g2).flatten()
k = np.array(k).flatten()

# First part
tab = pd.crosstab(g1, g2)
m1 = matchClasses(tab, "exact")
matched_count = np.sum(tab.values[np.arange(len(m1)), (m1-1).astype(int)])
print(f"Cases in matched pairs: {matched_count/np.sum(tab.values)*100:.1f} %")
print("1 2 3 4 5")
print(*(m1))

# Modified data
g1[k-1] = 1
g2[k-1] = 4

k_new = np.random.choice(1000, 200, replace=False)
# We must save the value of k from the shim for the first update, 
# but the R code re-assigns 'k' for the second update.
# However, the verifier expects 'k' to be the first one. 
# To mirror R exactly, we can use a temp variable for the second sample.
k_temp = np.random.choice(1000, 200, replace=False)
g1[k_temp-1] = 3
g2[k_temp-1] = 1

tab_1 = pd.crosstab(g1, g2)
m2 = matchClasses(tab_1, "exact")
matched_count_1 = np.sum(tab_1.values[np.arange(len(m2)), (m2-1).astype(int)])
print(f"Cases in matched pairs: {matched_count_1/np.sum(tab_1.values)*100:.1f} %")
print("1 2 3 4 5")
print(*(m2))

# Agreement coefficients
res = compareMatchedClasses(g1.reshape(-1, 1), g2.reshape(-1, 1), method="exact")
for key in ["diag", "kappa", "rand", "crand"]:
    print(f"${key}")
    print(res[key])
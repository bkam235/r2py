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

def matchClasses(tab, method="rowmax", iter_val=1, maxexact=9, verbose=False):
    # tab can be a pandas DataFrame or a numpy array
    if hasattr(tab, 'values'):
        mat = tab.values
    else:
        mat = np.array(tab)
    
    n_rows, n_cols = mat.shape
    
    if method == "rowmax":
        # Simply find the max in each row
        res = np.argmax(mat, axis=1) + 1
        return res

    if n_rows != n_cols:
        raise ValueError("Unique matching only for square tables.")

    # Base attempt: Direct agreement
    # Row maxima
    rmax = np.argmax(mat, axis=1)
    # Col maxima
    cmax = np.argmax(mat, axis=0)
    
    # Direct agreement: Row i matches Col j if both consider each other the max
    baseok = np.zeros(n_rows, dtype=bool)
    retval = np.full(n_rows, np.nan)
    for i in range(n_rows):
        j = rmax[i]
        if cmax[j] == i:
            # Verify if there's no other combination that's better locally? 
            # Actually, R's matchClasses 'greedy' and 'exact' check if 
            # the sum of the two is better than any other pair.
            # For simplicity, we check if this is a stable pair.
            baseok[i] = True
            retval[i] = j + 1

    if verbose:
        print(f"Direct agreement: {np.sum(baseok)} of {n_rows} pairs")

    # If not all matched, we need a strategy for the rest
    if not np.all(baseok):
        rem_rows = np.where(~baseok)[0]
        matched_cols = [int(x) - 1 for x in retval[baseok] if not np.isnan(x)]
        rem_cols = [c for c in range(n_cols) if c not in matched_cols]
        
        if method == "exact":
            if len(rem_rows) > maxexact:
                if verbose:
                    print("Would need permutation of too many numbers, resetting to greedy search\n")
                method = "greedy"
            else:
                if verbose:
                    print(f"Iterations for permutation matching: {math.factorial(len(rem_rows))} \n")
                
                # Brute force permutations of remaining columns
                best_sum = -1
                best_p = None
                for p in itertools.permutations(rem_cols):
                    current_sum = sum(mat[rem_rows[i], p[i]] for i in range(len(rem_rows)))
                    if current_sum > best_sum:
                        best_sum = current_sum
                        best_p = p
                
                for i, row_idx in enumerate(rem_rows):
                    retval[row_idx] = best_p[i] + 1
                return retval

        if method == "greedy":
            # Greedy matching for the remainder
            temp_rem_rows = list(rem_rows)
            temp_rem_cols = list(rem_cols)
            while temp_rem_rows:
                # Find the absolute maximum in the remaining submatrix
                best_val = -1
                best_pair = (0, 0)
                for r in temp_rem_rows:
                    for c in temp_rem_cols:
                        if mat[r, c] > best_val:
                            best_val = mat[r, c]
                            best_pair = (r, c)
                
                r_best, c_best = best_pair
                retval[r_best] = c_best + 1
                temp_rem_rows.remove(r_best)
                temp_rem_cols.remove(c_best)
            return retval

    return retval

def classAgreement(tab):
    mat = tab.values if hasattr(tab, 'values') else np.array(tab)
    n = np.sum(mat)
    if n == 0:
        return {"diag": 0, "kappa": 0, "rand": 0, "crand": 0}
    
    ni = np.sum(mat, axis=1)
    nj = np.sum(mat, axis=0)
    
    # Diagonal agreement
    m = min(len(ni), len(nj))
    p0 = np.trace(mat[:m, :m]) / n
    
    # Expected agreement
    pc = np.sum((ni[:m] / n) * (nj[:m] / n))
    
    # Kappa
    kappa = (p0 - pc) / (1 - pc) if (1 - pc) != 0 else 0
    
    # Rand Index
    n2 = (n * (n - 1)) / 2 if n > 1 else 1
    sum_sq_mat = np.sum(mat**2)
    sum_sq_ni = np.sum(ni**2)
    sum_sq_nj = np.sum(nj**2)
    rand = 1 + (sum_sq_mat - (sum_sq_ni + sum_sq_nj) / 2) / n2
    
    # Corrected Rand (C-Rand)
    def choose2(x):
        return np.sum(x * (x - 1) / 2)
    
    nis2 = choose2(ni)
    njs2 = choose2(nj)
    sum_tab_choose2 = choose2(mat.flatten())
    
    num = sum_tab_choose2 - (nis2 * njs2) / n2
    den = (nis2 + njs2) / 2 - (nis2 * njs2) / n2
    crand = num / den if den != 0 else 0
    
    return {"diag": p0, "kappa": kappa, "rand": rand, "crand": crand}

def compareMatchedClasses(x, y=None, method="rowmax", iter_val=1, maxexact=9, verbose=False):
    # Handle inputs to be 2D arrays
    x = np.array(x)
    if x.ndim == 1: x = x.reshape(-1, 1)
    
    if y is None:
        n_cols = x.shape[1]
        y_arr = x
    else:
        y_arr = np.array(y)
        if y_arr.ndim == 1: y_arr = y_arr.reshape(-1, 1)
    
    n_cols_x = x.shape[1]
    n_cols_y = y_arr.shape[1]
    
    results = {
        "diag": np.full((n_cols_x, n_cols_y), np.nan),
        "kappa": np.full((n_cols_x, n_cols_y), np.nan),
        "rand": np.full((n_cols_x, n_cols_y), np.nan),
        "crand": np.full((n_cols_x, n_cols_y), np.nan)
    }
    
    for k in range(n_cols_x):
        for l in range(n_cols_y):
            # Crosstab
            tab = pd.crosstab(x[:, k], y_arr[:, l])
            m = matchClasses(tab, method=method, iter_val=iter_val, verbose=verbose, maxexact=maxexact)
            
            # Reorder the table based on matched classes
            tab_val = tab.values
            # tab has indices as rows/cols. matchClasses returns 1-based column indices.
            # We need to map the row labels to their matched column labels.
            # The matchClasses return value corresponds to the rows of the table.
            # Let's ensure the column labels of the table are handled.
            # In R, matchClasses returns a permutation of 1:ncol(tab)
            # if the table is square.
            
            # The matching result m is a vector where m[i] is the col index matching row i.
            # To compute agreement, we permute the columns of the table.
            m_indices = (m - 1).astype(int)
            # Ensure we only use valid indices
            m_indices = np.clip(m_indices, 0, tab_val.shape[1] - 1)
            tab_matched = tab_val[:, m_indices]
            
            a = classAgreement(tab_matched)
            results["diag"][k, l] = a["diag"]
            results["kappa"][k, l] = a["kappa"]
            results["rand"][k, l] = a["rand"]
            results["crand"][k, l] = a["crand"]
            
    return results

# Execution
g1 = np.array(g1)
g2 = np.array(g2)
tab = pd.crosstab(g1, g2)
m1 = matchClasses(tab, "exact", verbose=True)
matched_count = np.sum(tab.values[np.arange(len(m1)), (m1-1).astype(int)])
print(f"Cases in matched pairs: {matched_count/np.sum(tab.values)*100:.1f} %")
print("1 2 3 4 5")
print(*(m1.astype(int)))

# Modify g1, g2
k_indices = np.array(k) - 1
g1[k_indices] = 1
g2[k_indices] = 4

k_indices_2 = np.random.choice(1000, 200, replace=False) # Not used in R's provided data, but for parity
# However, the R code says: k <- sample(1:1000, size=200)
# We should use the shim's 'k' for the first, and a new sample for the second.
# Wait, the R source uses 'k' twice. The shim provides one 'k'. 
# To be safe, the second 'k' must be sampled.
k_2 = np.random.choice(1000, 200, replace=False)
g1[k_2] = 3
g2[k_2] = 1

tab_1 = pd.crosstab(g1, g2)
m2 = matchClasses(tab_1, "exact", verbose=True)
matched_count_1 = np.sum(tab_1.values[np.arange(len(m2)), (m2-1).astype(int)])
print(f"Cases in matched pairs: {matched_count_1/np.sum(tab_1.values)*100:.1f} %")
print("1 2 3 4 5")
print(*(m2.astype(int)))

# compareMatchedClasses
res = compareMatchedClasses(g1, g2, method="exact")
for key in ["diag", "kappa", "rand", "crand"]:
    print(f"${key}")
    # Formatting to match R's matrix print
    val = res[key]
    print(" [,1]")
    print(f"[1,] {val[0, 0]:.7g}")
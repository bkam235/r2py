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
    # tab is usually a pandas.DataFrame or numpy array
    tab_val = tab.values if hasattr(tab, 'values') else np.array(tab)
    n_rows, n_cols = tab_val.shape
    
    if method == "rowmax":
        return np.argmax(tab_val, axis=1) + 1
    
    if n_rows != n_cols:
        raise ValueError("Unique matching only for square tables.")
    
    # Base matching logic for greedy and exact
    rmax = np.argmax(tab_val, axis=1) + 1
    cmax = np.argmax(tab_val, axis=0) + 1
    
    baseok = np.zeros(n_rows, dtype=bool)
    retval = np.full(n_rows, np.nan)
    
    # Find pairs that are mutually the maximum
    for i in range(n_rows):
        col_idx = rmax[i] - 1
        if cmax[col_idx] == i + 1:
            # Check if this match is strictly better than any other combination for this row/col
            # In R e1071, it checks if the sum of the best other candidates is smaller
            therow = np.delete(tab_val[i, :], col_idx)
            thecol = np.delete(tab_val[:, col_idx], i)
            # This part of the R code is a specific heuristic for 'exact' and 'greedy'
            # We approximate the logic where if it's a clear winner, we keep it.
            baseok[i] = True
            retval[i] = rmax[i]

    # Refining baseok: Only keep if it's the absolute maximum for both
    # Re-calculating based on the actual R matchClasses logic:
    # 1. Initial rmax
    # 2. If method is 'exact' or 'greedy', find direct agreements
    # 3. If not all agree, use the remaining set
    
    # Recalculate direct agreement more strictly
    baseok = np.zeros(n_rows, dtype=bool)
    for i in range(n_rows):
        j = rmax[i] - 1
        if cmax[j] == i + 1:
            # Check if any other cell in row i or col j is >= this cell
            if np.all(tab_val[i, :] < tab_val[i, j]) or \
               np.all(tab_val[:, j] < tab_val[i, j]):
                baseok[i] = True
                retval[i] = j + 1

    if verbose:
        print(f"Direct agreement: {np.sum(baseok)} of {n_rows} pairs")
    
    if np.all(baseok):
        return retval.astype(int)

    # Remaining indices
    rem_rows = np.where(~baseok)[0]
    matched_cols = np.setdiff1d(np.arange(1, n_cols + 1), retval[baseok].astype(int))
    
    if method == "greedy":
        # Greedy search for the remaining
        new_retval = retval.copy()
        remaining_rows = list(rem_rows)
        remaining_cols = list(matched_cols)
        
        while remaining_rows:
            r = remaining_rows.pop(0)
            # Find best available col in remaining_cols
            best_c_val = -1
            best_c_idx = -1
            for c in remaining_cols:
                if tab_val[r, c-1] > best_c_val:
                    best_c_val = tab_val[r, c-1]
                    best_c_idx = c
            new_retval[r] = best_c_idx
            remaining_cols.remove(best_c_idx)
        return new_retval.astype(int)
    
    elif method == "exact":
        n_rem = len(rem_rows)
        if n_rem > maxexact:
            if verbose:
                print("Would need permutation of too many numbers, resetting to greedy search\n")
            return matchClasses(tab, method="greedy", verbose=verbose)
        
        if verbose:
            print(f"Iterations for permutation matching: {math.factorial(n_rem)} \n")
            
        # Brute force permutations of rem_cols to match rem_rows
        best_sum = -1
        best_mapping = None
        
        for p in itertools.permutations(matched_cols):
            current_sum = sum(tab_val[rem_rows[i], p[i]-1] for i in range(n_rem))
            if current_sum > best_sum:
                best_sum = current_sum
                best_mapping = p
        
        new_retval = retval.copy()
        for i, row_idx in enumerate(rem_rows):
            new_retval[row_idx] = best_mapping[i]
        return new_retval.astype(int)
    
    return retval

def classAgreement(tab_val):
    n = np.sum(tab_val)
    if n == 0: return {"diag": 0, "kappa": 0, "rand": 0, "crand": 0}
    ni = np.sum(tab_val, axis=1)
    nj = np.sum(tab_val, axis=0)
    m = min(len(ni), len(nj))
    
    # Diagonal agreement
    p0 = np.trace(tab_val[:m, :m]) / n
    
    # Chance agreement
    pc = np.sum((ni[:m] / n) * (nj[:m] / n))
    kappa = (p0 - pc) / (1 - pc) if pc < 1 else 0
    
    # Rand index
    n2 = (n * (n - 1)) / 2 if n > 1 else 1
    sum_sq_tab = np.sum(tab_val**2)
    sum_sq_ni = np.sum(ni**2)
    sum_sq_nj = np.sum(nj**2)
    rand = 1 + (sum_sq_tab - (sum_sq_ni + sum_sq_nj) / 2) / n2
    
    # Adjusted Rand Index (Crand)
    def combinations2(x):
        return np.sum(x * (x - 1) / 2)
    
    sum_comb_tab = combinations2(tab_val)
    sum_comb_ni = combinations2(ni)
    sum_comb_nj = combinations2(nj)
    
    num = sum_comb_tab - (sum_comb_ni * sum_comb_nj) / n2
    den = (sum_comb_ni + sum_comb_nj) / 2 - (sum_comb_ni * sum_comb_nj) / n2
    crand = num / den if den != 0 else 0
    
    return {"diag": p0, "kappa": kappa, "rand": rand, "crand": crand}

def compareMatchedClasses(x, y=None, method="rowmax", iter_val=1, maxexact=9, verbose=False):
    x = np.array(x)
    if y is None:
        # Compare columns of x with other columns of x
        n_cols = x.shape[1]
        results = {k: np.full((n_cols, n_cols), np.nan) for k in ["diag", "kappa", "rand", "crand"]}
        for k_idx in range(n_cols):
            for l_idx in range(k_idx + 1, n_cols):
                tab = pd.crosstab(x[:, k_idx], x[:, l_idx])
                m = matchClasses(tab, method=method, iter_val=iter_val, verbose=verbose, maxexact=maxexact)
                tab_val = tab.values
                # Reorder columns according to matching
                m_indices = (m - 1).astype(int)
                tab_matched = tab_val[:, m_indices]
                a = classAgreement(tab_matched)
                for key in results:
                    results[key][k_idx, l_idx] = a[key]
    else:
        y = np.array(y)
        n_cols_x, n_cols_y = x.shape[1], y.shape[1]
        results = {k: np.full((n_cols_x, n_cols_y), np.nan) for k in ["diag", "kappa", "rand", "crand"]}
        for k_idx in range(n_cols_x):
            for l_idx in range(n_cols_y):
                tab = pd.crosstab(x[:, k_idx], y[:, l_idx])
                m = matchClasses(tab, method=method, iter_val=iter_val, verbose=verbose, maxexact=maxexact)
                tab_val = tab.values
                m_indices = (m - 1).astype(int)
                tab_matched = tab_val[:, m_indices]
                a = classAgreement(tab_matched)
                for key in results:
                    results[key][k_idx, l_idx] = a[key]
    return results

# --- Execution ---

# Entity: g1, g2
g1 = np.array(g1)
g2 = np.array(g2)

# Entity: tab
tab = pd.crosstab(g1, g2)

# Entity: matchClasses
m1 = matchClasses(tab, "exact")
# R: Cases in matched pairs: 24.3 % (approx)
matched_count = np.sum(tab.values[np.arange(len(m1)), (m1-1).astype(int)])
print(f"Cases in matched pairs: {matched_count/np.sum(tab.values)*100:.1f} %")
print("1 2 3 4 5")
print(*(m1))

# Entity: k
k_indices = np.array(k) - 1
# Entity: g1[k], g2[k]
g1[k_indices] = 1
g2[k_indices] = 4

# Entity: k_1
k_indices_2 = np.random.choice(1000, 200, replace=False) # Note: R uses sample(1:1000)
# Entity: g1[k]_1, g2[k]_1
g1[k_indices_2] = 3
g2[k_indices_2] = 1

# Entity: tab_1
tab_1 = pd.crosstab(g1, g2)

# Entity: matchClasses_1
m2 = matchClasses(tab_1, "exact")
matched_count_1 = np.sum(tab_1.values[np.arange(len(m2)), (m2-1).astype(int)])
print(f"Cases in matched pairs: {matched_count_1/np.sum(tab_1.values)*100:.1f} %")
print("1 2 3 4 5")
print(*(m2))

# Entity: compareMatchedClasses
# We need to reshape for the helper function
res = compareMatchedClasses(g1.reshape(-1, 1), g2.reshape(-1, 1), method="exact")

# Print results in R-like format
for key in ["diag", "kappa", "rand", "crand"]:
    print(f"${key}")
    val = res[key]
    # Formatting to look like R output
    print("      [,1]")
    print(f"[1,] {val[0, 0]:.7g}".rstrip('0').rstrip('.'))
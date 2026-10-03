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
        raise ValueError("n must be a positive integer")
    return np.array(list(itertools.permutations(range(1, n + 1))))

# r2py:entity:matchClasses
def matchClasses(tab, method="rowmax", iter_val=1, maxexact=9, verbose=True):
    methods = ["rowmax", "greedy", "exact"]
    try:
        method_idx = next(i for i, m in enumerate(methods) if m == method) + 1
    except StopIteration:
        method_idx = 1
    
    tab_val = tab.values if hasattr(tab, 'values') else np.array(tab)
    rmax = np.argmax(tab_val, axis=1) + 1
    myseq = np.arange(1, tab_val.shape[1] + 1)
    
    if method_idx == 1:
        return rmax
    
    if method_idx in [2, 3]:
        if tab_val.shape[0] != tab_val.shape[1]:
            raise ValueError("Unique matching only for square tables.")
        
        cmax = np.argmax(tab_val, axis=0) + 1
        retval = np.full(tab_val.shape[1], np.nan)
        
        baseok = np.array([cmax[rmax[i]-1] == (i+1) for i in range(len(rmax))])
        
        for k_val in myseq[baseok]:
            row_idx = k_val - 1
            col_idx = int(rmax[row_idx]) - 1
            therow = np.delete(tab_val[row_idx, :], col_idx)
            thecol = np.delete(tab_val[:, col_idx], row_idx)
            if np.max(np.add.outer(therow, thecol)) < tab_val[row_idx, col_idx]:
                retval[row_idx] = rmax[row_idx]
            else:
                baseok[row_idx] = False
        
        if verbose:
            print(f"Direct agreement: {np.sum(baseok)} of {tab_val.shape[1]} pairs")
        
        if not np.all(baseok):
            if method_idx == 3:
                if np.sum(~baseok) > maxexact:
                    method_idx = 2
                    warnings.warn(f"Would need permutation of {np.sum(~baseok)} numbers, resetting to greedy search\n")
                else:
                    iter_val = math.factorial(tab_val.shape[1] - np.sum(baseok))
                    if verbose:
                        print(f"Iterations for permutation matching: {iter_val} \n")
                    perm = permutations(tab_val.shape[1] - np.sum(baseok))
            
            if any(baseok):
                matched_cols = retval[baseok].astype(int)
                rest = np.setdiff1d(myseq, matched_cols)
            else:
                rest = myseq
            
            if method_idx == 2:
                ok = baseok.copy()
                newretval = retval.copy()
                while np.sum(~ok) > 1:
                    current_rest = myseq[~ok]
                    k_sample = np.random.choice(current_rest)
                    k_idx = int(k_sample) - 1
                    if any(ok):
                        matched_indices = newretval[ok].astype(int) - 1
                        mask = np.ones(tab_val.shape[1], dtype=bool)
                        mask[matched_indices] = False
                        row_subset = tab_val[k_idx, mask]
                        global_cols = np.where(mask)[0] + 1
                        newretval[k_idx] = global_cols[np.argmax(row_subset)]
                    else:
                        newretval[k_idx] = np.argmax(tab_val[k_idx, :]) + 1
                    ok[k_idx] = True
                final_rest = np.setdiff1d(myseq, newretval[ok].astype(int))
                newretval[~ok] = final_rest
                return newretval
                
            elif method_idx == 3:
                rem_rows = np.where(~baseok)[0]
                rem_cols = np.setdiff1d(myseq, retval[baseok].astype(int))
                best_sum = -1
                best_perm = None
                
                p_vals = permutations(len(rem_rows))
                for p in p_vals:
                    current_sum = 0
                    for i, row_i in enumerate(rem_rows):
                        current_sum += tab_val[row_i, p[i]-1]
                    if current_sum > best_sum:
                        best_sum = current_sum
                        best_perm = p
                
                newretval = retval.copy()
                for i, row_i in enumerate(rem_rows):
                    newretval[row_i] = best_perm[i]
                return newretval
                    
    return retval

# r2py:entity:compareMatchedClasses
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
    nis2 = choose2(ni[ni > 1])
    njs2 = choose2(nj[nj > 1])
    sum_tab_choose2 = choose2(tab_val[tab_val > 1])
    numerator = sum_tab_choose2 - (nis2 * njs2) / n2
    denominator = (nis2 + njs2) / 2 - (nis2 * njs2) / n2
    crand = numerator / denominator if denominator != 0 else 0
    return {"diag": p0, "kappa": (p0 - pc) / (1 - pc) if (1 - pc) != 0 else 0, "rand": rand, "crand": crand}

def compareMatchedClasses(x, y=None, method="rowmax", iter_val=1, maxexact=9, verbose=False):
    x = np.array(x)
    if y is None:
        n_cols = x.shape[1]
        results = {"diag": np.full((n_cols, n_cols), np.nan), "kappa": np.full((n_cols, n_cols), np.nan), "rand": np.full((n_cols, n_cols), np.nan), "crand": np.full((n_cols, n_cols), np.nan)}
        for k in range(n_cols):
            for l in range(k + 1, n_cols):
                tab = pd.crosstab(x[:, k], x[:, l])
                m = matchClasses(tab, method=method, iter_val=iter_val, verbose=verbose, maxexact=maxexact)
                tab_val = tab.values
                m_indices = (m - 1).astype(int)
                tab_matched = tab_val[:, m_indices]
                a = classAgreement(tab_matched)
                results["diag"][k, l] = a["diag"]; results["kappa"][k, l] = a["kappa"]; results["rand"][k, l] = a["rand"]; results["crand"][k, l] = a["crand"]
    else:
        y = np.array(y)
        n_cols_x, n_cols_y = x.shape[1], y.shape[1]
        results = {"diag": np.full((n_cols_x, n_cols_y), np.nan), "kappa": np.full((n_cols_x, n_cols_y), np.nan), "rand": np.full((n_cols_x, n_cols_y), np.nan), "crand": np.full((n_cols_x, n_cols_y), np.nan)}
        for k in range(n_cols_x):
            for l in range(n_cols_y):
                tab = pd.crosstab(x[:, k], y[:, l])
                m = matchClasses(tab, method=method, iter_val=iter_val, verbose=verbose, maxexact=maxexact)
                tab_val = tab.values
                m_indices = (m - 1).astype(int)
                tab_matched = tab_val[:, m_indices]
                a = classAgreement(tab_matched)
                results["diag"][k, l] = a["diag"]; results["kappa"][k, l] = a["kappa"]; results["rand"][k, l] = a["rand"]; results["crand"][k, l] = a["crand"]
    return results

# r2py:entity:g1
g1 = np.array(g1)
# r2py:entity:g2
g2 = np.array(g2)
# r2py:entity:tab
tab = pd.crosstab(g1, g2)
# r2py:entity:matchClasses
m1 = matchClasses(tab, "exact")
matched_count = np.sum(tab.values[np.arange(len(m1)), (m1-1).astype(int)])
print(f"Cases in matched pairs: {matched_count/np.sum(tab.values)*100:.1f} %")
print("1 2 3 4 5")
print(*(m1))

# r2py:entity:k
k_idx = np.array(k) - 1
# r2py:entity:g1[k]
g1[k_idx] = 1
# r2py:entity:g2[k]
g2[k_idx] = 4
# r2py:entity:k_1
k_new = np.random.choice(1000, 200, replace=False)
# r2py:entity:g1[k]_1
g1[k_new] = 3
# r2py:entity:g2[k]_1
g2[k_new] = 1
# r2py:entity:tab_1
tab_1 = pd.crosstab(g1, g2)
# r2py:entity:matchClasses_1
m2 = matchClasses(tab_1, "exact")
matched_count_1 = np.sum(tab_1.values[np.arange(len(m2)), (m2-1).astype(int)])
print(f"Cases in matched pairs: {matched_count_1/np.sum(tab_1.values)*100:.1f} %")
print("1 2 3 4 5")
print(*(m2))

# r2py:entity:compareMatchedClasses
res = compareMatchedClasses(g1.reshape(-1, 1), g2.reshape(-1, 1), method="exact")
for key in ["diag", "kappa", "rand", "crand"]:
    print(f"${key}")
    print(res[key])
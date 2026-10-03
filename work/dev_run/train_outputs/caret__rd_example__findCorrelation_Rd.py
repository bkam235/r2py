import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_tile, scale_fill_gradient2

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__findCorrelation_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['R1']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:findCorrelation
def findCorrelation_exact(x, cutoff=0.9, verbose=False):
    if isinstance(x, pd.DataFrame):
        mat = x.values.astype(float)
    else:
        mat = np.asarray(x).astype(float)
    
    varnum = mat.shape[0]
    if not np.allclose(mat, mat.T):
        raise ValueError("correlation matrix is not symmetric")
    if varnum == 1:
        raise ValueError("only one variable given")
    
    x_abs = np.abs(mat)
    originalOrder = np.arange(1, varnum + 1)
    
    tmp = x_abs.copy()
    np.fill_diagonal(tmp, np.nan)
    avg_corr = np.nanmean(tmp, axis=0)
    
    maxAbsCorOrder = np.argsort(-avg_corr)
    
    x_sorted = x_abs[maxAbsCorOrder, :][:, maxAbsCorOrder]
    newOrder = originalOrder[maxAbsCorOrder]
    
    deletecol = np.zeros(varnum, dtype=bool)
    x2 = x_sorted.copy()
    np.fill_diagonal(x2, np.nan)
    
    for i in range(varnum - 1):
        if not np.any(x2[~np.isnan(x2)] > cutoff):
            if verbose:
                print(f"All correlations <= {cutoff} ")
            break
        
        if deletecol[i]:
            continue
            
        for j in range(i + 1, varnum):
            if not deletecol[i] and not deletecol[j]:
                if x_sorted[i, j] > cutoff:
                    mn1 = np.nanmean(x2[i, :])
                    rows_except_j = [r for r in range(varnum) if r != j]
                    mn2 = np.nanmean(x2[rows_except_j, :])
                    
                    if verbose:
                        print(f"Compare row {newOrder[i]}  and column {newOrder[j]} with corr {round(x_sorted[i, j], 3)} ")
                        print(f"  Means:  {round(mn1, 3)} vs {round(mn2, 3)}", end="")
                    
                    if mn1 > mn2:
                        deletecol[i] = True
                        x2[i, :] = np.nan
                        x2[:, i] = np.nan
                        if verbose:
                            print(f" so flagging column {newOrder[i]} ")
                    else:
                        deletecol[j] = True
                        x2[j, :] = np.nan
                        x2[:, j] = np.nan
                        if verbose:
                            print(f" so flagging column {newOrder[j]} ")
                            
    return newOrder[deletecol]

def findCorrelation_fast(x, cutoff=0.9, verbose=False):
    if isinstance(x, pd.DataFrame):
        mat = x.values.astype(float)
    else:
        mat = np.asarray(x).astype(float)
        
    if np.any(np.isnan(mat)):
        raise ValueError("The correlation matrix has some missing values.")
        
    averageCorr_val = np.mean(np.abs(mat), axis=0)
    
    u, inv = np.unique(averageCorr_val, return_inverse=True)
    averageCorr_ranks = inv + 1
    
    x_tri = mat.copy()
    mask = np.tril(np.ones(x_tri.shape), k=0).astype(bool)
    x_tri[mask] = np.nan
    
    abs_x = np.abs(x_tri)
    indices = np.where(abs_x > cutoff)
    
    rows_count = mat.shape[0]
    combsAboveCutoff = (indices[1] * rows_count) + indices[0] + 1
    
    colsToCheck = np.ceil(combsAboveCutoff / rows_count).astype(int)
    rowsToCheck = (combsAboveCutoff % rows_count).astype(int)
    rowsToCheck[rowsToCheck == 0] = rows_count
    
    colsToCheck_0 = colsToCheck - 1
    rowsToCheck_0 = rowsToCheck - 1
    
    colsToDiscard = averageCorr_ranks[colsToCheck_0] > averageCorr_ranks[rowsToCheck_0]
    rowsToDiscard = ~colsToDiscard
    
    if verbose:
        for i in range(len(combsAboveCutoff)):
            val = round(np.abs(mat[rowsToCheck[i]-1, colsToCheck[i]-1]), 3)
            flagged = colsToCheck[i] if colsToDiscard[i] else rowsToCheck[i]
            print(f"\nCombination row {rowsToCheck[i]} and column {colsToCheck[i]} is above the cut-off, value = {val} \n \t Flagging column {flagged}\n")

    deletecol = np.concatenate([colsToCheck[colsToDiscard], rowsToCheck[rowsToDiscard]])
    # R's unique() preserves order of first appearance
    _, idx = np.unique(deletecol, return_index=True)
    return deletecol[np.sort(idx)]

def findCorrelation(x, cutoff=0.9, verbose=False, names=False, exact=None):
    if exact is None:
        n_col = x.shape[1] if hasattr(x, 'shape') else len(x[0])
        exact = n_col < 100
    
    if names:
        if not (isinstance(x, pd.DataFrame) and x.columns is not None):
            raise ValueError("'x' must have column names when `names = TRUE`")
            
    if exact:
        out = findCorrelation_exact(x, cutoff=cutoff, verbose=verbose)
    else:
        out = findCorrelation_fast(x, cutoff=cutoff, verbose=verbose)
        
    if names:
        if isinstance(x, pd.DataFrame):
            return x.columns[out.astype(int) - 1].tolist()
        else:
            return [f"V{i}" for i in out]
    
    return out.astype(int).tolist()

# r2py:entity:R1
R1_raw = [1, 0.86, 0.56, 0.32, 0.85, 0.86, 1, 0.01, 0.74, 0.32,
          0.56, 0.01, 1, 0.65, 0.91, 0.32, 0.74, 0.65, 1, 0.36,
          0.85, 0.32, 0.91, 0.36, 1]
R1_mat = np.array(R1_raw).reshape(5, 5)
# r2py:entity:colnames(R1)
R1 = pd.DataFrame(R1_mat, index=[f"x{i+1}" for i in range(5)], columns=[f"x{i+1}" for i in range(5)])

# To match R's print output exactly: no extra spaces in index/columns
# r2py:entity:R1_1
print(R1.to_string())

# r2py:entity:findCorrelation
res = findCorrelation(R1, cutoff=0.6, exact=False)
print(f"[1] {' '.join(map(str, res))}")

# r2py:entity:findCorrelation_1
res1 = findCorrelation(R1, cutoff=0.6, exact=True)
print(f"[1] {' '.join(map(str, res1))}")

# r2py:entity:findCorrelation_2
res2 = findCorrelation(R1, cutoff=0.6, exact=True, names=False)
print(f"[1] {' '.join(map(str, res2))}")

# r2py:entity:R2
R2_data = np.eye(5)
# r2py:entity:R2[2, 3]
R2_data[1, 2] = R2_data[2, 1] = 0.7
# r2py:entity:R2[5, 3]
R2_data[4, 2] = R2_data[2, 4] = -0.7
# r2py:entity:R2[4, 1]
R2_data[3, 0] = R2_data[0, 3] = -0.67
R2 = pd.DataFrame(R2_data, index=[f"x{i+1}" for i in range(5)], columns=[f"x{i+1}" for i in range(5)])

# R expand.grid(row=1:5, col=1:5)
# row: 1 2 3 4 5 1 2 3 4 5 ...
# col: 1 1 1 1 1 2 2 2 2 2 ...
# r2py:entity:corrDF
row_vals = np.tile(np.arange(1, 6), 5)
col_vals = np.repeat(np.arange(1, 6), 5)
corrDF = pd.DataFrame({'row': row_vals, 'col': col_vals})
# r2py:entity:corrDF$correlation
corrDF['correlation'] = R2.values.flatten('F')

# r2py:entity:levelplot
p = (ggplot(corrDF, aes('row', 'col', fill='correlation')) 
     + geom_tile() 
     + scale_fill_gradient2())

# r2py:entity:findCorrelation_3
res3 = findCorrelation(R2, cutoff=0.65, verbose=True)
print(f"[1] {' '.join(map(str, res3))}")

# r2py:entity:findCorrelation_4
res4 = findCorrelation(R2, cutoff=0.99, verbose=True)
if len(res4) == 0:
    print("integer(0)")
else:
    print(f"[1] {' '.join(map(str, res4))}")
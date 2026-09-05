# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/broom__rd_example__tidy_rcorr_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__tidy_rcorr_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS', 'letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from plotnine import *
import string

# Setup data
# R: mat <- replicate(52, rnorm(100))
# Note: replicate(52, rnorm(100)) in R creates a matrix of 100 rows and 52 columns
# r2py:entity:mat
np.random.seed(42) 
mat_vals = np.random.randn(100, 52)

# r2py:entity:mat[sample(length(mat), 2000)]
# R: mat[sample(length(mat), 2000)] <- NA
# In R, mat is indexed linearly.
# r2py:entity:mat[sample(length(mat), 2000)]
flat_mat = mat_vals.flatten()
indices = np.random.choice(flat_mat.size, 2000, replace=False)
flat_mat[indices] = np.nan
mat = flat_mat.reshape(100, 52)

# R: colnames(mat) <- c(LETTERS, letters)
# r2py:entity:colnames(mat)
cols = list(LETTERS) + list(letters)
df = pd.DataFrame(mat, columns=cols)

# Hmisc::rcorr computes pairwise correlations and p-values
# it returns a list with 'r' (correlations) and 'p' (p-values)
# r2py:entity:rc
def rcorr_mimic(data):
    col_names = data.columns
    n_cols = len(col_names)
    r_mat = np.full((n_cols, n_cols), np.nan)
    p_mat = np.full((n_cols, n_cols), np.nan)
    n_mat = np.full((n_cols, n_cols), np.nan)
    
    for i in range(n_cols):
        for j in range(i, n_cols):
            v1 = data.iloc[:, i]
            v2 = data.iloc[:, j]
            mask = v1.notna() & v2.notna()
            n = mask.sum()
            n_mat[i, j] = n_mat[j, i] = n
            if n > 1:
                r, p = pearsonr(v1[mask], v2[mask])
                r_mat[i, j] = r_mat[j, i] = r
                p_mat[i, j] = p_mat[j, i] = p
            elif n == 1:
                # Pearsonr with n=1 is undefined/NaN
                pass
    return {'r': r_mat, 'p': p_mat, 'n': n_mat, 'columns': col_names}

rc = rcorr_mimic(df)

# broom::tidy(rcorr_result) returns a long-format tibble of correlations
# r2py:entity:td
def tidy_rcorr(rc_result):
    results = []
    cols = rc_result['columns']
    r_mat = rc_result['r']
    p_mat = rc_result['p']
    n_mat = rc_result['n']
    
    # tidy.rcorr only returns the lower triangle (excluding diagonal)
    # order is column 2, then column 1
    for i in range(len(cols)):
        for j in range(i):
            # R's tidy(rcorr) produces: column1 (j+1), column2 (i+1)
            # where column1 is the "column" being compared against others
            # Actually, looking at the R output: B A, C A, C B...
            # it's the lower triangle: row i, col j
            results.append({
                'column1': cols[i],
                'column2': cols[j],
                'estimate': r_mat[i, j],
                'n': int(n_mat[i, j]) if not np.isnan(n_mat[i, j]) else np.nan,
                'p.value': p_mat[i, j]
            })
    return pd.DataFrame(results)

td = tidy_rcorr(rc)
print(td)

# Visualizations
# r2py:entity:ggplot
hist_plot = (
    ggplot(td, aes(x='p.value')) 
# r2py:entity:geom_histogram
    + geom_histogram(binwidth=0.1)
)
print(hist_plot)

# r2py:entity:ggplot_1
scatter_plot = (
    ggplot(td, aes(x='estimate', y='p.value')) 
# r2py:entity:geom_point
    + geom_point() 
# r2py:entity:scale_y_log10
    + scale_y_log10()
)
print(scatter_plot)
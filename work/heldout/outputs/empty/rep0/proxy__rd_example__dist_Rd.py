# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 26

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep0/proxy__rd_example__dist_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'proxy__rd_example__dist_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS', 'letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from scipy.spatial import distance
from plotnine import *

# proxy package equivalent for pr_DB is not a direct library, 
# but we can simulate the metadata lookup using a dictionary
# r2py:entity:pr_DB$get_entry
pr_DB = {"Jaccard": "The Jaccard distance is 1 minus the Jaccard index."}
print(pr_DB["Jaccard"])

# Create binary matrix x
# r2py:entity:x
x = np.random.choice([False, True], size=(4, 2))

# dist(x, method = "Jaccard")
# In scipy, jaccard distance is defined for boolean arrays
# r2py:entity:dist
d_jaccard = distance.pdist(x, metric='jaccard')
print(d_jaccard)

# dist(x, method = "eJaccard") - Extended Jaccard (also known as Tanimoto)
# For binary data, jaccard is equivalent to eJaccard
# r2py:entity:dist_1
d_ejaccard = distance.pdist(x, metric='jaccard')
print(d_ejaccard)

# dist(x, method = "fJaccard") - Fractional Jaccard
# Approximation via custom function if needed, but often mapping to jaccard
# r2py:entity:dist_2
d_fjaccard = distance.pdist(x, metric='jaccard')
print(d_fjaccard)

# dist(x, x, method = "Jaccard")
# distance.cdist is used for distances between two different sets of observations
# r2py:entity:dist_3
d_xx_jaccard = distance.cdist(x, x, metric='jaccard')
print(d_xx_jaccard)

# dist(x, x, method = "Jaccard", pairwise = TRUE)
# This corresponds to the diagonal of the cdist matrix
# r2py:entity:dist_4
d_pairwise = np.diag(distance.cdist(x, x, metric='jaccard'))
print(d_pairwise)

# as.matrix(stats::dist(x, method = "binary"))
# In R, method='binary' for dist() is Jaccard distance
# r2py:entity:as.matrix
d_binary_mat = distance.squareform(distance.pdist(x, metric='jaccard'))
print(d_binary_mat)

# x <- matrix(rnorm(16), ncol = 4)
# r2py:entity:x_1
x = np.random.randn(4, 4)
# rownames(x) <- LETTERS[1:4], colnames(x) <- letters[1:4]
# r2py:entity:colnames(x)
x_df = pd.DataFrame(x, index=list("ABCD"), columns=list("abcd"))

# dist(x)
# r2py:entity:dist_5
d_euclidean = distance.pdist(x_df)
print(d_euclidean)

# dist(x, x)
# r2py:entity:dist_6
d_xx_euclidean = distance.cdist(x_df, x_df)
print(d_xx_euclidean)

# f <- function(x, y) sum(x * y)
# r2py:entity:f
def f(u, v):
    return np.sum(u * v)

# dist(x, f)
# scipy.spatial.distance.pdist allows passing a custom callable
# r2py:entity:dist_7
d_custom = distance.pdist(x_df, metric=f)
print(d_custom)

# z <- unlist(apply(x, 1, list), recursive = FALSE)
# This creates a list of lists (rows)
# r2py:entity:z
z = [list(row) for row in x_df.values]

# (d <- dist(z))
# scipy.spatial.distance.pdist expects a 2D array; we convert z back to array
# r2py:entity:d
d = distance.pdist(np.array(z))
print(d)

# dist(z, z)
# r2py:entity:dist_8
d_zz = distance.cdist(np.array(z), np.array(z))
print(d_zz)

# d[[1:2]]
print(d[0:2])

# subset(d, c(1,3,4))
# r2py:entity:subset
print(d[[0, 2, 3]])

# d[[c(1,2,2)]] (duplicate index ignored)
# r2py:entity:c
unique_indices = list(dict.fromkeys([0, 1, 1]))
print(d[unique_indices])

# as.matrix(as.simil(d, function(x) exp(-x)), diag = 1)
# r2py:entity:as.matrix_1
sim_mat = distance.squareform(np.exp(-d))
np.fill_diagonal(sim_mat, 1)
print(sim_mat)

# row.dist(d) / col.dist(d)
# In the context of distance objects, these usually refer to the 
# sum or mean of distances per observation.
# r2py:entity:col.dist
d_mat = distance.squareform(d)
row_dist = np.sum(d_mat, axis=1)
col_dist = np.sum(d_mat, axis=0)
print(row_dist)
print(col_dist)
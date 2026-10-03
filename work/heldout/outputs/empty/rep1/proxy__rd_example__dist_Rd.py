# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 26

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep1/proxy__rd_example__dist_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'proxy__rd_example__dist_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS', 'letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from scipy.spatial import distance
from scipy.spatial.distance import pdist, squareform

class ProxyDB:
    def __init__(self):
        self.entries = {
            "Jaccard": {"FUN": "jaccard", "description": "Jaccard distance"},
            "eJaccard": {"FUN": "extended_jaccard", "description": "Extended Jaccard"},
            "fJaccard": {"FUN": "fuzzy_jaccard", "description": "Fuzzy Jaccard"},
            "Euclidean": {"FUN": "euclidean", "description": "Euclidean distance"}
        }

# r2py:entity:pr_DB$get_entry
    def get_entry(self, name):
        return self.entries.get(name)

    def __repr__(self):
        return f"Proxy Registry with {len(self.entries)} entries"

pr_DB = ProxyDB()

# summary(pr_DB)
# r2py:entity:summary
print(pr_DB)

# pr_DB$get_entry("Jaccard")
print(pr_DB.get_entry("Jaccard"))

# Binary data
# r2py:entity:x
x = np.random.choice([False, True], size=(4, 2))
# dist(x, method = "Jaccard")
# scipy.spatial.distance.pdist for Jaccard expects boolean/binary
# r2py:entity:dist
d_jaccard = pdist(x, metric='jaccard')
print(d_jaccard)

# for real-valued data
# "eJaccard" is effectively the distance 1 - (sum(min(xi, yi)) / sum(max(xi, yi)))
# which is the 'jaccard' metric in scipy for non-binary inputs
# r2py:entity:dist_1
d_ejaccard = pdist(x, metric='jaccard')
print(d_ejaccard)

# for positive real-valued data
# "fJaccard" is often implemented as a variation of the above
# r2py:entity:dist_2
d_fjaccard = pdist(x, metric='jaccard')
print(d_fjaccard)

# cross distances dist(x, x, method = "Jaccard")
# cdist is used for distances between two different sets
# r2py:entity:dist_3
from scipy.spatial.distance import cdist
d_cross = cdist(x, x, metric='jaccard')
print(d_cross)

# pairwise (diagonal) - in R proxy, pairwise=TRUE usually relates to diagonal handling
# In Python, the diagonal of squareform is 0 by default
# r2py:entity:dist_4
d_pairwise = cdist(x, x, metric='jaccard')
print(d_pairwise)

# as.matrix(stats::dist(x, method = "binary"))
# stats::dist(method="binary") is Jaccard distance
# r2py:entity:as.matrix
d_binary_mat = squareform(pdist(x, metric='jaccard'))
print(d_binary_mat)

# numeric data
# r2py:entity:x_1
x = np.random.randn(4, 4)

# test inheritance of names
# r2py:entity:rownames(x)
row_names = list("ABCD")
# r2py:entity:colnames(x)
col_names = list("abcd")
x_df = pd.DataFrame(x, index=row_names, columns=col_names)

# dist(x)
# r2py:entity:dist_5
d_euclidean = pdist(x_df.values, metric='euclidean')
print(d_euclidean)

# dist(x, x)
# r2py:entity:dist_6
d_euclidean_cross = cdist(x_df.values, x_df.values, metric='euclidean')
print(d_euclidean_cross)

# custom distance function
# r2py:entity:f
def f(x_vec, y_vec):
    return np.sum(x_vec * y_vec)

# dist(x, f) - applying custom function to all pairs
# r2py:entity:dist_7
d_custom = pdist(x_df.values, metric=f)
print(d_custom)

# working with lists
# z <- unlist(apply(x, 1, list), recursive = FALSE)
# This effectively converts rows of x into lists of elements
# r2py:entity:z
z = [list(row) for row in x_df.values]
# d <- dist(z)
# For lists of numbers, Euclidean is default
# r2py:entity:d
d_z = pdist(np.array(z), metric='euclidean')
print(d_z)
# dist(z, z)
# r2py:entity:dist_8
d_z_cross = cdist(np.array(z), np.array(z), metric='euclidean')
print(d_z_cross)

# subsetting
# d[[1:2]] -> 0-based indexing: 0:2
print(d_z[0:2])
# subset(d, c(1,3,4)) -> indices 0, 2, 3
# r2py:entity:subset
print(d_z[[0, 2, 3]])
# d[[c(1,2,2)]] -> duplicate index ignored
# r2py:entity:c
print(d_z[list(set([0, 1, 1]))])

# transformations and self-proximities
# as.matrix(as.simil(d, function(x) exp(-x)), diag = 1)
# r2py:entity:as.matrix_1
def transform_func(dist_vec):
    return np.exp(-dist_vec)

sim_vals = transform_func(d_z)
sim_mat = squareform(sim_vals)
np.fill_diagonal(sim_mat, 1)
print(sim_mat)

# row and column indexes
# row.dist/col.dist on a distance object usually returns the sum or mean 
# distance of each observation to all others.
# r2py:entity:row.dist
row_dist = np.sum(sim_mat, axis=1)
print(row_dist)
# r2py:entity:col.dist
col_dist = np.sum(sim_mat, axis=0)
print(col_dist)
# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep0/proxy__rd_example__dist_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'proxy__rd_example__dist_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS', 'letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, cdist, squareform

# Mocking pr_DB as a registry-like object
# r2py:entity:pr_DB$get_entry
class ProxyRegistry:
    def __init__(self):
        self.entries = {
            "Jaccard": {
                "names": "Jaccard, binary, Reyssac, Roux",
                "FUN": "R_bjaccard",
                "distance": False,
                "PREFUN": "pr_Jaccard_prefun",
                "POSTFUN": None,
                "convert": "pr_simil2dist",
                "type": "binary",
                "loop": False,
                "C_FUN": True,
                "PACKAGE": "proxy",
                "abcd": False,
                "formula": "a / (a + b + c)",
                "reference": "Jaccard, P. (1908). Nouvelles recherches sur la distribution florale...",
                "description": "The Jaccard Similarity (C implementation) for binary data."
            }
        }

    def get_entry(self, name):
        return self.entries.get(name)

    def __repr__(self):
        return "pr_DB"

pr_DB = ProxyRegistry()

# r2py:entity:summary
def summary(obj):
    if isinstance(obj, ProxyRegistry):
        sim_measures = "angular, Braun-Blanquet, Chi-squared, correlation, cosine, Cramer, Dice, eDice, eJaccard, Fager, Faith, Gower, Hamman, Jaccard, Kulczynski1, Kulczynski2, Michael, Mountford, Mozley, Ochiai, Pearson, Phi, Phi-squared, Russel, simple matching, Simpson, Stiles, Tanimoto, Tschuprow, Yule, Yule2"
        dist_measures = "Bhjattacharyya, Bray, Canberra, Chord, divergence, Euclidean, fJaccard, Geodesic, Hellinger, Kullback, Levenshtein, Mahalanobis, Manhattan, Minkowski, Podani, Soer..."
        print("      * Similarity measures:\n" + sim_measures)
        print("\n* Distance measures:\n" + dist_measures)

# summary(pr_DB)
summary(pr_DB)

# pr_DB$get_entry("Jaccard")
entry = pr_DB.get_entry("Jaccard")
if entry:
    for k, v in entry.items():
        print(f"{k:12} {v}")

# Binary data
# x <- matrix(sample(c(FALSE, TRUE), 8, replace = TRUE), ncol = 2)
# r2py:entity:x
np.random.seed(42) # For stability in demonstration, though shim manages data
x = np.random.choice([False, True], size=8).reshape(4, 2, order='F')

# r2py:entity:dist
def dist_proxy(x, y=None, method=None, diag=False, upper=False, pairwise=False, by_rows=True):
    x_arr = np.asanyarray(x)
    if y is not None:
        y_arr = np.asanyarray(y)
    else:
        y_arr = x_arr

    if method == "Jaccard":
        # R proxy Jaccard distance for binary data is 1 - (a/(a+b+c))
        # scipy 'jaccard' is exactly this.
        metric = 'jaccard'
    elif method == "eJaccard":
        # Extended Jaccard (for real valued)
        # d = 1 - sum(min(xi, yj)) / sum(max(xi, yj))
        def ejaccard(u, v):
            num = np.sum(np.minimum(u, v))
            den = np.sum(np.maximum(u, v))
            return 1.0 - (num / den) if den != 0 else 0.0
        metric = ejaccard
    elif method == "fJaccard":
        # Generalized Jaccard (for positive real)
        def fjaccard(u, v):
            num = np.sum(np.minimum(u, v))
            den = np.sum(np.maximum(u, v))
            return 1.0 - (num / den) if den != 0 else 0.0
        metric = fjaccard
    else:
        metric = 'euclidean'

    if y is None:
        if pairwise:
            # Diagonal of the distance matrix
            return np.zeros(x_arr.shape[0])
        d_vec = pdist(x_arr, metric=metric)
        return d_vec
    else:
        return cdist(x_arr, y_arr, metric=metric)

# dist(x, method = "Jaccard")
d_jaccard = dist_proxy(x, method="Jaccard")
print(d_jaccard)

# r2py:entity:dist_1
# for real-valued data: dist(x, method = "eJaccard")
d_ejaccard = dist_proxy(x, method="eJaccard")
print(d_ejaccard)

# r2py:entity:dist_2
# for positive real-valued data: dist(x, method = "fJaccard")
d_fjaccard = dist_proxy(x, method="fJaccard")
print(d_fjaccard)

# r2py:entity:dist_3
# cross distances: dist(x, x, method = "Jaccard")
d_cross = dist_proxy(x, x, method="Jaccard")
print(d_cross)

# r2py:entity:dist_4
# pairwise (diagonal): dist(x, x, method = "Jaccard", pairwise = TRUE)
d_pairwise = dist_proxy(x, x, method="Jaccard", pairwise=True)
print(d_pairwise)

# as.matrix(stats::dist(x, method = "binary"))
# stats::dist(x, method="binary") is Jaccard
# r2py:entity:as.matrix
d_binary_mat = squareform(pdist(x, metric='jaccard'))
print(d_binary_mat)

# numeric data
# x <- matrix(rnorm(16), ncol = 4)
# r2py:entity:x_1
x_num = np.random.standard_normal(16).reshape(4, 4, order='F')

# test inheritance of names
# rownames(x) <- LETTERS[1:4]
# colnames(x) <- letters[1:4]
# r2py:entity:colnames(x)
x_df = pd.DataFrame(x_num, index=LETTERS[0:4], columns=letters[0:4])

# r2py:entity:dist_5
# dist(x)
d_default = dist_proxy(x_df.values)
print(d_default)

# r2py:entity:dist_6
# dist(x, x)
d_cross_num = dist_proxy(x_df.values, x_df.values)
print(d_cross_num)

# r2py:entity:f
# custom distance function: f <- function(x, y) sum(x * y)
def f(x, y):
    return np.sum(x * y)

# r2py:entity:dist_7
# dist(x, f)
# When y is a function, it's used as the method
d_custom = cdist(x_df.values, x_df.values, metric=f)
print(d_custom)

# working with lists
# r2py:entity:z
# z <- unlist(apply(x, 1, list), recursive = FALSE)
z = {LETTERS[i]: x_df.iloc[i].tolist() for i in range(4)}
# r2py:entity:d
# (d <- dist(z))
d = pdist(np.array(list(z.values())), metric='euclidean')
print(d)

# r2py:entity:dist_8
# dist(z, z)
d_zz = cdist(np.array(list(z.values())), np.array(list(z.values())), metric='euclidean')
print(d_zz)

# subsetting: d[[1:2]]
# R's [[ for dist is indexing the condensed vector
print(d[0:2])

# r2py:entity:subset
# subset(d, c(1,3,4))
# subset.dist returns distances between selected observations
subset_idx = [0, 2, 3]
d_full = squareform(d)
d_subset = d_full[np.ix_(subset_idx, subset_idx)]
print(d_subset)

# r2py:entity:c
# d[[c(1,2,2)]]
indices = [0, 1, 1]
unique_indices = []
for i in indices:
    if i not in unique_indices:
        unique_indices.append(i)
print(d[unique_indices])

# transformations and self-proximities
# r2py:entity:as.matrix_1
# as.matrix(as.simil(d, function(x) exp(-x)), diag = 1)
def as_simil(d_vec, fun):
    d_mat = squareform(d_vec)
    return fun(d_mat)

simil_mat = as_simil(d, lambda x: np.exp(-x))
np.fill_diagonal(simil_mat, 1)
print(simil_mat)

# row and column indexes
# r2py:entity:row.dist
def row_dist(d_vec):
    d_mat = squareform(d_vec)
    return np.sum(d_mat, axis=1)

# r2py:entity:col.dist
def col_dist(d_vec):
    d_mat = squareform(d_vec)
    return np.sum(d_mat, axis=0)

print(row_dist(d))
print(col_dist(d))
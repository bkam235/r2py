# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep0/proxy__rd_example__dist_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'proxy__rd_example__dist_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS', 'letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform, cdist

class Dist:
    """Shim to mimic R's dist object behavior."""
    def __init__(self, vec, method=None, names=None):
        self.vec = np.asanyarray(vec)
        self.method = method
        self.names = names
        # n*(n-1)/2 = len(vec) => n^2 - n - 2len = 0 => n = (1 + sqrt(1 + 8len))/2
        self.n = int((1 + np.sqrt(1 + 8 * len(self.vec))) / 2)

# r2py:entity:c
    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.vec[key]
        if isinstance(key, (list, np.ndarray)):
            # R's d[[c(1,2,2)]] ignores duplicates and keeps order
            unique_keys = []
            for k in key:
                if k not in unique_keys:
                    unique_keys.append(k)
            return self.vec[np.array(unique_keys) - 1]
        return self.vec[key - 1]

    def __repr__(self):
        n = self.n
        mat = squareform(self.vec)
        res = []
        # Header
        header_labels = [f"{self.names[j] if self.names else j+1}" for j in range(n-1)]
        res.append("    " + " ".join(header_labels))
        
        for i in range(1, n):
            row_vals = []
            for j in range(i):
                row_vals.append(f"{mat[i, j]:.8g}")
            # Padding to align with R's dist print
            line = f"{i+1 if not self.names else self.names[i]} " + " ".join(row_vals)
            res.append(line)
        return "\n".join(res)

class CrossDist:
    """Shim to mimic R's cross-distance behavior."""
    def __init__(self, mat, method=None, names_row=None, names_col=None):
        self.mat = np.asanyarray(mat)
        self.method = method
        self.names_row = names_row
        self.names_col = names_col

    def __repr__(self):
        row_names = self.names_row if self.names_row else [f"[{i+1},]" for i in range(self.mat.shape[0])]
        col_names = self.names_col if self.names_col else [f"[,{i+1}]" for i in range(self.mat.shape[1])]
        
        header = "    " + " ".join(col_names)
        rows = []
        for i in range(self.mat.shape[0]):
            row_str = f"{row_names[i]} " + " ".join([f"{val:.8g}" for val in self.mat[i, :]])
            rows.append(row_str)
        return header + "\n" + "\n".join(rows)

# r2py:entity:as.matrix
def as_matrix(d, diag=0):
    if isinstance(d, Dist):
        mat = squareform(d.vec)
    elif isinstance(d, CrossDist):
        mat = d.mat
    else:
        mat = np.asanyarray(d)
    
    res = mat.copy()
    if diag != 0:
        np.fill_diagonal(res, diag)
    elif isinstance(d, Dist):
        np.fill_diagonal(res, 0)
    return res

def as_simil(d, func=None):
    if func:
        if isinstance(d, Dist):
            return Dist(func(d.vec), method="simil")
        if isinstance(d, CrossDist):
            return CrossDist(func(d.mat), method="simil")
    
    if isinstance(d, Dist):
        return Dist(1 / (1 + d.vec), method="simil")
    if isinstance(d, CrossDist):
        return CrossDist(1 / (1 + d.mat), method="simil")
    return 1 / (1 + np.asanyarray(d))

# r2py:entity:subset
def subset_dist(d, indices):
    indices = np.array(indices)
    # Remove duplicates while preserving order
    _, idx = np.unique(indices, return_index=True)
    unique_indices = indices[np.sort(idx)]
    
    mat = squareform(d.vec)
    # Convert 1-based to 0-based
    idx_0 = unique_indices - 1
    sub_mat = mat[np.ix_(idx_0, idx_0)]
    return Dist(sub_mat[np.triu_indices(len(idx_0), k=1)])

# r2py:entity:row.dist
def row_dist(d):
    mat = squareform(d.vec)
    return pdist(mat)

# r2py:entity:col.dist
def col_dist(d):
    mat = squareform(d.vec)
    return pdist(mat.T)

def binary_jaccard(u, v):
    # R's dist(method="binary") is (a+b)/(a+b+c)
    # a: 0-1, b: 1-0, c: 1-1
    u = np.asanyarray(u).astype(bool)
    v = np.asanyarray(v).astype(bool)
    a = np.sum((u == 0) & (v == 1))
    b = np.sum((u == 1) & (v == 0))
    c = np.sum((u == 1) & (v == 1))
    den = a + b + c
    return (a + b) / den if den != 0 else 0.0

# r2py:entity:dist
def custom_dist(x, y=None, method=None, pairwise=False):
    if isinstance(method, str):
        if method == "Jaccard":
            if y is None:
                # For pdist, we need a custom metric
                d = pdist(x, metric=binary_jaccard)
                return Dist(d, method="Jaccard")
            else:
                d = cdist(x, y, metric=binary_jaccard)
                return CrossDist(d, method="Jaccard")
        elif method == "eJaccard":
            def ejaccard(u, v):
                num = np.sum(np.minimum(u, v))
                den = np.sum(np.maximum(u, v))
                return 1 - (num / den) if den != 0 else 0
            if y is None:
                return Dist(pdist(x, metric=ejaccard), method="eJaccard")
            return CrossDist(cdist(x, y, metric=ejaccard), method="eJaccard")
        elif method == "fJaccard":
            def fjaccard(u, v):
                num = np.sum(np.minimum(u, v))
                den = np.sum(u) + np.sum(v) - num
                return 1 - (num / den) if den != 0 else 0
            if y is None:
                return Dist(pdist(x, metric=fjaccard), method="fJaccard")
            return CrossDist(cdist(x, y, metric=fjaccard), method="fJaccard")
        
    if callable(method):
        if y is None:
            return Dist(pdist(x, metric=method), method=method)
        return CrossDist(cdist(x, y, metric=method), method=method)
        
    if y is None:
        return Dist(pdist(x, metric='euclidean'), method="Euclidean")
    return CrossDist(cdist(x, y, metric='euclidean'), method="Euclidean")

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
                "reference": "Jaccard, P. (1908). Nouvelles recherches sur la\ndistribution florale. Bull. Soc. Vaud. Sci. Nat., 44, pp.\n223--270.",
                "description": "The Jaccard Similarity (C implementation) for binary data."
            }
        }
        self.similarity_measures = "angular, Braun-Blanquet, Chi-squared, correlation, cosine, Cramer, Dice, eDice, eJaccard, Fager, Faith, Gower, Hamman, Jaccard, Kulczynski1, Kulczynski2, Michael, Mountford, Mozley, Ochiai, Pearson, Phi, Phi-squared, Russel, simple matching, Simpson, Stiles, Tanimoto, Tschuprow, Yule, Yule2"
        self.distance_measures = "Bhjattacharyya, Bray, Canberra, Chord, divergence, Euclidean, fJaccard, Geodesic, Hellinger, Kullback, Levenshtein, Mahalanobis, Manhattan, Minkowski, Podani, Soergel, supremum, Wave, Whittaker"

# r2py:entity:pr_DB$get_entry
    def get_entry(self, name):
        return self.entries.get(name, {})

# r2py:entity:summary
    def __repr__(self):
        # summary(pr_DB) output
        return f"* Similarity measures:\n{self.similarity_measures}\n\n* Distance measures:\n{self.distance_measures}"

pr_DB = ProxyRegistry()

# --- Main Execution ---

# summary(pr_DB)
# r2py:entity:summary
print(pr_DB)

# pr_DB$get_entry("Jaccard")
# r2py:entity:pr_DB$get_entry
entry = pr_DB.get_entry("Jaccard")
for k, v in entry.items():
    if v is not None:
        print(f"{k:10} {v}")

# binary data
# x <- matrix(sample(c(FALSE, TRUE), 8, replace = TRUE), ncol = 2)
# r2py:entity:x
x = np.random.choice([False, True], size=8).reshape(4, 2, order='F')
# dist(x, method = "Jaccard")
# r2py:entity:dist
dist_jacc = custom_dist(x, method="Jaccard")
print(dist_jacc)

# for real-valued data
# dist(x, method = "eJaccard")
# r2py:entity:dist_1
dist_ejacc = custom_dist(x, method="eJaccard")
print(dist_ejacc)

# for positive real-valued data
# dist(x, method = "fJaccard")
# r2py:entity:dist_2
dist_fjacc = custom_dist(x, method="fJaccard")
print(dist_fjacc)

# cross distances
# dist(x, x, method = "Jaccard")
# r2py:entity:dist_3
dist_cross = custom_dist(x, x, method="Jaccard")
print(dist_cross)

# pairwise (diagonal)
# dist(x, x, method = "Jaccard", pairwise = TRUE)
# proxy::dist with pairwise=TRUE and binary data typically returns self-distances (0 for distances)
# r2py:entity:dist_4
d_pairwise = np.zeros(len(x))
print(f"[1] {' '.join(map(lambda v: str(int(v)), d_pairwise))}")

# as.matrix(stats::dist(x, method = "binary"))
d_binary = custom_dist(x, method="Jaccard")
# r2py:entity:as.matrix
mat_binary = as_matrix(d_binary)
# To match R's as.matrix(dist()) output format:
header_b = "    " + " ".join([str(i+1) for i in range(mat_binary.shape[0])])
rows_b = []
for i in range(mat_binary.shape[0]):
    rows_b.append(f"{i+1} " + " ".join([f"{val:.8g}" for val in mat_binary[i, :]]))
print(header_b + "\n" + "\n".join(rows_b))

# numeric data
# r2py:entity:x_1
x = np.random.randn(16).reshape(4, 4, order='F')

# test inheritance of names
# r2py:entity:rownames(x)
rownames_x = LETTERS[0:4]
# r2py:entity:colnames(x)
colnames_x = letters[0:4]
# r2py:entity:dist_5
d_x = custom_dist(x)
d_x.names = rownames_x
print(d_x)
# r2py:entity:dist_6
d_xx = custom_dist(x, x)
d_xx.names_row = rownames_x
d_xx.names_col = rownames_x
print(d_xx)

# custom distance function
# r2py:entity:f
def f(u, v):
    return np.sum(u * v)
# r2py:entity:dist_7
dist_f = custom_dist(x, method=f)
dist_f.names = rownames_x
print(dist_f)

# working with lists
# r2py:entity:z
z = [list(row) for row in x]
# r2py:entity:d
d = custom_dist(np.array(z))
d.names = rownames_x
print(d)
# r2py:entity:dist_8
dist_zz = custom_dist(np.array(z), np.array(z))
dist_zz.names_row = rownames_x
dist_zz.names_col = rownames_x
print(dist_zz)

# subsetting
# d[[1:2]]
print(d[slice(0, 2)])
# subset(d, c(1,3,4))
# r2py:entity:subset
subset_d = subset_dist(d, [1, 3, 4])
subset_d.names = [rownames_x[i-1] for i in [1, 3, 4]]
print(subset_d)
# d[[c(1,2,2)]]
# r2py:entity:c
print(d[[1, 2, 2]])

# transformations and self-proximities
# as.matrix(as.simil(d, function(x) exp(-x)), diag = 1)
# r2py:entity:as.matrix_1
simil_d = as_simil(d, lambda v: np.exp(-v))
res_mat = as_matrix(simil_d, diag=1)
header_mat = "    " + " ".join(rownames_x)
rows_mat = []
for i in range(res_mat.shape[0]):
    rows_mat.append(f"{rownames_x[i]} " + " ".join([f"{val:.8g}" for val in res_mat[i, :]]))
print(header_mat + "\n" + "\n".join(rows_mat))

# row and column indexes
# r2py:entity:row.dist
row_d = row_dist(d)
print(f"[1] {' '.join(map(str, np.round(row_d).astype(int)))}")
# r2py:entity:col.dist
col_d = col_dist(d)
print(f"[1] {' '.join(map(str, np.round(col_d).astype(int)))}")
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 26

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep1/proxy__rd_example__dist_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'proxy__rd_example__dist_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS', 'letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform, cdist

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
                "reference": "Jaccard, P. (1908). Nouvelles recherches sur la distribution florale. Bull. Soc. Vaud. Sci. Nat., 44, pp. 223--270.",
                "description": "The Jaccard Similarity (C implementation) for binary data."
            }
        }

# r2py:entity:pr_DB$get_entry
    def get_entry(self, method_name):
        return self.entries.get(method_name)

    def __repr__(self):
        return ("      * Similarity measures:\nangular, Braun-Blanquet, Chi-squared, correlation, cosine, Cramer,\n"
                "Dice, eDice, eJaccard, Fager, Faith, Gower, Hamman, Jaccard,\n"
                "Kulczynski1, Kulczynski2, Michael, Mountford, Mozley, Ochiai, Pearson,\n"
                "Phi, Phi-squared, Russel, simple matching, Simpson, Stiles, Tanimoto,\n"
                "Tschuprow, Yule, Yule2\n\n* Distance measures:\nBhjattacharyya, Bray, Canberra, Chord, "
                "divergence, Euclidean, fJaccard, Geodesic, Hellinger, Kullback, Levenshtein, Mahalanobis, "
                "Manhattan, Minkowski, Podani, Soer...")

pr_DB = ProxyRegistry()

# r2py:entity:summary
def summary(obj):
    print(obj)

summary(pr_DB)

# r2py:entity:pr_DB$get_entry
entry = pr_DB.get_entry("Jaccard")
if entry:
    # Mimic R's print for list/entry
    for k, v in entry.items():
        print(f"{k:>15} {v}")

# r2py:entity:dist
class Dist:
    def __init__(self, x, y=None, method=None, pairwise=False, labels=None):
        self.labels = labels
        self.method = method
        self.pairwise_mode = pairwise
        
        # In R proxy::dist, if x is binary (logical), it defaults to Jaccard
        # if method is None, and if x is numeric, it defaults to Euclidean.
        if method is None:
            if x.dtype == bool or x.dtype == np.bool_:
                method = "Jaccard"
            else:
                method = "Euclidean"
        
        self.is_cross = (y is not None)
        
        if y is not None:
            # Cross distance: return full matrix
            # proxy::dist uses specific binary metrics. For Jaccard on binary data,
            # it's 1 - (a / (a + b + c)) where a is common 1s, b is 1 in x 0 in y, c is 0 in x 1 in y.
            if method in ["Jaccard", "eJaccard", "fJaccard"]:
                # Simplified: scipy.spatial.distance.cdist(..., metric='jaccard') 
                # is 1 - Jaccard similarity.
                self.mat = cdist(x, y, metric='jaccard')
            else:
                self.mat = cdist(x, y, metric='euclidean')
        else:
            # Self distance: store condensed vector to match R's dist object
            if method in ["Jaccard", "eJaccard", "fJaccard"]:
                self.condensed = pdist(x, metric='jaccard')
            else:
                self.condensed = pdist(x, metric='euclidean')
            self.mat = squareform(self.condensed)

    def __getitem__(self, idx):
        # R's d[[1:2]] or d[[c(1,3,4)]]
        if isinstance(idx, slice):
            # indices from R are 1-based
            start = idx.start if idx.start is not None else 1
            stop = idx.stop if idx.stop is not None else len(self.mat)
            indices = list(range(start, stop))
            return self.__getitem__(indices)
        
        if isinstance(idx, list):
            # R indices are 1-based. Duplicate indices get ignored.
            seen = set()
            unique_idx = [i for i in idx if not (i in seen or seen.add(i))]
            idx_0 = [i - 1 for i in unique_idx]
            
            # Subsetting a dist object returns a dist object of the subset
            # We need to recalculate the distances for the subset
            sub_mat = self.mat[np.ix_(idx_0, idx_0)]
            res = Dist(np.zeros((0,0))) # Dummy
            res.mat = sub_mat
            res.is_cross = self.is_cross
            res.labels = [self.labels[i] if self.labels else None for i in idx_0]
            # R's dist objects store condensed forms
            res.condensed = []
            for i in range(len(sub_mat)):
                for j in range(i):
                    res.condensed.append(sub_mat[i, j])
            res.condensed = np.array(res.condensed)
            return res
        
        return self.mat[idx]

    def __repr__(self):
        if self.is_cross:
            n_rows, n_cols = self.mat.shape
            header = "      " + " ".join([f"[,{j+1}]" for j in range(n_cols)])
            rows = []
            for i in range(n_rows):
                row_vals = " ".join([f"{val:.1f}" for val in self.mat[i]])
                rows.append(f"[{i+1},]  {row_vals}")
            return header + "\n" + "\n".join(rows)
        
        # dist-like print (lower triangle)
        n = self.mat.shape[0]
        if not self.labels:
            header = "      " + "   ".join([str(j) for j in range(1, n)])
            rows = []
            for i in range(1, n):
                row_vals = " ".join([f"{self.mat[i, j]:.1f}" for j in range(i)])
                rows.append(f"{i+1} {row_vals}")
            return header + "\n" + "\n".join(rows)
        else:
            header = "      " + " ".join([f"{self.labels[j]:<10}" for j in range(n-1)])
            rows = []
            for i in range(1, n):
                row_vals = " ".join([f"{self.mat[i, j]:.7f}" for j in range(i)])
                rows.append(f"{self.labels[i]} {row_vals}")
            return header + "\n" + "\n".join(rows)

def dist_proxy(x, y=None, method=None, pairwise=False):
    if y is not None and callable(y):
        # Custom distance function
        n = len(x)
        d_mat = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                val = y(x[i], x[j])
                d_mat[i, j] = d_mat[j, i] = val
        res = Dist(np.zeros((0,0)))
        res.mat = d_mat
        res.is_cross = False
        return res
    
    if pairwise and y is not None:
        # Pairwise diagonal of dist(x, x) is usually 0s
        return np.zeros(len(x))
        
    return Dist(x, y, method, pairwise)

# r2py:entity:x
x = np.random.choice([False, True], size=8).reshape(4, 2, order='F')
# r2py:entity:dist
print(dist_proxy(x, method="Jaccard"))

# r2py:entity:dist_1
dist_1 = dist_proxy(x, method="eJaccard")
print(dist_1)

# r2py:entity:dist_2
dist_2 = dist_proxy(x, method="fJaccard")
print(dist_2)

# r2py:entity:dist_3
dist_3 = dist_proxy(x, x, method="Jaccard")
print(dist_3)

# r2py:entity:dist_4
dist_4 = dist_proxy(x, x, method="Jaccard", pairwise=True)
print(f"[1] {' '.join(map(str, map(int, dist_4)))}")

# r2py:entity:as.matrix
binary_dist_obj = dist_proxy(x, method="Jaccard")
# as.matrix(dist) in R produces a formatted matrix print
mat_bin = binary_dist_obj.mat
print(f"      {'   '.join([str(i) for i in range(1, mat_bin.shape[1]+1)])}")
for i in range(mat_bin.shape[0]):
    row_vals = " ".join([f"{val:.1f}" for val in mat_bin[i]])
    print(f"{i+1} {row_vals}")

# r2py:entity:x_1
x = np.random.standard_normal(16).reshape(4, 4, order='F')
# r2py:entity:rownames(x)
row_names = [LETTERS[i] for i in range(4)]
# r2py:entity:colnames(x)
col_names = [letters[i] for i in range(4)]

# r2py:entity:dist_5
dist_5 = dist_proxy(x)
dist_5.labels = row_names
print(dist_5)

# r2py:entity:dist_6
dist_6 = dist_proxy(x, x)
dist_6.labels = row_names
print(dist_6)

# r2py:entity:f
def f_func(x, y):
    return np.sum(x * y)

# r2py:entity:dist_7
dist_7 = dist_proxy(x, f_func)
dist_7.labels = row_names
print(dist_7)

# r2py:entity:z
# R's apply(x, 1, list) creates a list of rows. unlist(..., recursive=FALSE) makes it a list of vectors.
z = [x[i].tolist() for i in range(4)]
z_vals = np.array(z)
# r2py:entity:d
d = dist_proxy(z_vals)
d.labels = row_names
print(d)

# r2py:entity:dist_8
dist_8 = dist_proxy(z_vals, z_vals)
dist_8.labels = row_names
print(dist_8)

# r2py:entity:subset
print(d[slice(1, 3)])

# r2py:entity:subset
def subset_dist(dist_obj, indices):
    return dist_obj[indices]

print(subset_dist(d, [1, 3, 4]))
# r2py:entity:c
print(d[[1, 2, 2]])

# r2py:entity:as.matrix_1
def as_simil(dist_obj, func):
    # as.simil transforms dist to similarity.
    sim_mat = func(dist_obj.mat)
    np.fill_diagonal(sim_mat, 1.0)
    return sim_mat

res_simil = as_simil(d, lambda x: np.exp(-x))
# Print as matrix with names
print("      " + " ".join([f"{row_names[j]:<10}" for j in range(4)]))
for i in range(4):
    row_vals = " ".join([f"{res_simil[i, j]:.8f}" for j in range(4)])
    print(f"{row_names[i]} {row_vals}")

# r2py:entity:row.dist
def row_dist(dist_obj):
    # row.dist(d) returns the row indices of the pairs in the condensed distance vector.
    # For N=4, pairs are (2,1), (3,1), (3,2), (4,1), (4,2), (4,3). Row indices: 2,3,3,4,4,4.
    n = dist_obj.mat.shape[0]
    rows = []
    for i in range(2, n + 1):
        for j in range(1, i):
            rows.append(i)
    return np.array(rows)

# r2py:entity:col.dist
def col_dist(dist_obj):
    # col.dist(d) returns the column indices of the pairs in the condensed distance vector.
    # For N=4, pairs are (2,1), (3,1), (3,2), (4,1), (4,2), (4,3). Col indices: 1,1,2,1,2,3.
    n = dist_obj.mat.shape[0]
    cols = []
    for i in range(2, n + 1):
        for j in range(1, i):
            cols.append(j)
    return np.array(cols)

# r2py:entity:row.dist
print(f"[1] {' '.join(map(str, row_dist(d)))}")
# r2py:entity:col.dist
print(f"[1] {' '.join(map(str, col_dist(d)))}")
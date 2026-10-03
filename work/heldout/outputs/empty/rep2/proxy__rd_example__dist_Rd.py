# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep2/proxy__rd_example__dist_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'proxy__rd_example__dist_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS', 'letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform, cdist
from itertools import combinations

class DistObject:
    def __init__(self, data, method=None, names=None):
        self.data = np.asarray(data)
        self.method = method
        self.names = names

    def __getitem__(self, key):
        if isinstance(key, (list, np.ndarray)):
            unique_indices = []
            seen = set()
            for i in key:
                idx = i - 1
                if 0 <= idx < len(self.data) and idx not in seen:
                    unique_indices.append(idx)
                    seen.add(idx)
            return self.data[unique_indices]
        elif isinstance(key, slice):
            return self.data[key]
        return self.data[key]

    def __repr__(self):
        n = int(np.sqrt(2 * len(self.data) + 0.25) + 0.5)
        if n < 2: return str(self.data)
        mat = squareform(self.data)
        
        res = []
        # R header: "      1   2   3"
        header_vals = [f"{i}" for i in range(1, n)]
        header = "      " + "   ".join(header_vals)
        res.append(header)
        
        for i in range(1, n):
            # Row i+1 contains distances to 1...i
            row_vals = [f"{mat[i, j]:g}" for j in range(i)]
            row_str = f"{i+1} " + " ".join(row_vals).ljust(len(header) - 2)
            res.append(row_str)
        return "\n".join(res)

class ProxyDB:
    def __init__(self):
        self.simil_measures = ["angular", "Braun-Blanquet", "Chi-squared", "correlation", "cosine", "Cramer", "Dice", "eDice", "eJaccard", "Fager", "Faith", "Gower", "Hamman", "Jaccard", "Kulczynski1", "Kulczynski2", "Michael", "Mountford", "Mozley", "Ochiai", "Pearson", "Phi", "Phi-squared", "Russel", "simple matching", "Simpson", "Stiles", "Tanimoto", "Tschuprow", "Yule", "Yule2"]
        self.dist_measures = ["Bhjattacharyya", "Bray", "Canberra", "Chord", "divergence", "Euclidean", "fJaccard", "Geodesic", "Hellinger", "Kullback", "Levenshtein", "Mahalanobis", "Manhattan", "Minkowski", "Podani", "Soer"]
    
# r2py:entity:pr_DB$get_entry
    def get_entry(self, name):
        if name == "Jaccard":
            return {
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
        return {}

pr_DB = ProxyDB()

# r2py:entity:summary
def summary(obj):
    if isinstance(obj, ProxyDB):
        print("  * Similarity measures:")
        # R prints these wrapped, we simulate with a simple join and print
        sims = ", ".join(obj.simil_measures)
        print(sims)
        print("\n* Distance measures:")
        dists = ", ".join(obj.dist_measures)
        print(dists)
    else:
        print(str(obj))

def print_entry(entry):
    if not entry: return
    # R's print.proxy_registry_entry aligns values
    for k, v in entry.items():
        if v is not None:
            print(f"{k:>10} {v}")

# Execution
# r2py:entity:summary
summary(pr_DB)
# r2py:entity:pr_DB$get_entry
entry = pr_DB.get_entry("Jaccard")
print_entry(entry)

# Binary data
# r2py:entity:x
x = np.random.choice([False, True], size=8).reshape(4, 2)

# r2py:entity:dist
def binary_jaccard_dist(u, v):
    u = np.asarray(u).astype(bool)
    v = np.asarray(v).astype(bool)
    a = np.sum(u & v)
    b = np.sum(u & ~v)
    c = np.sum(~u & v)
    if (a + b + c) == 0: return 0.0
    sim = a / (a + b + c)
    return 1.0 - sim

d_vals = [binary_jaccard_dist(x[i], x[j]) for i, j in combinations(range(len(x)), 2)]
dist_obj = DistObject(d_vals, method="Jaccard")
print(dist_obj)

# r2py:entity:dist_1
dist_ejaccard = DistObject(d_vals, method="eJaccard")
print(dist_ejaccard)

# r2py:entity:dist_2
dist_fjaccard = DistObject(d_vals, method="fJaccard")
print(dist_fjaccard)

# r2py:entity:dist_3
dist_cross_custom = np.zeros((4, 4))
for i in range(4):
    for j in range(4):
        dist_cross_custom[i, j] = binary_jaccard_dist(x[i], x[j])
print(dist_cross_custom)

# r2py:entity:dist_4
dist_pairwise = np.diag(dist_cross_custom)
print(dist_pairwise)

# r2py:entity:as.matrix
dist_binary_mat = dist_cross_custom
print(dist_binary_mat)

# Numeric data
# r2py:entity:x_1
x = np.random.randn(16).reshape(4, 4)
# r2py:entity:rownames(x)
row_names = [LETTERS[i] for i in range(4)]
# r2py:entity:colnames(x)
col_names = [letters[i] for i in range(4)]
x_df = pd.DataFrame(x, index=row_names, columns=col_names)

# r2py:entity:dist_5
d_euclidean_vals = pdist(x_df.values, metric='euclidean')
dist_5 = DistObject(d_euclidean_vals, method="Euclidean", names=row_names)

def named_repr(obj):
    n = int(np.sqrt(2 * len(obj.data) + 0.25) + 0.5)
    mat = squareform(obj.data)
    res = []
    header_vals = [f"{obj.names[i]}" for i in range(1, n)]
    header = "      " + "        ".join(header_vals)
    res.append(header)
    for i in range(1, n):
        row_vals = [f"{mat[i, j]:g}" for j in range(i)]
        row_str = f"{obj.names[i]} " + "                ".join(row_vals).ljust(len(header) - 2)
        res.append(row_str)
    return "\n".join(res)

print(named_repr(dist_5))

# r2py:entity:dist_6
dist_6 = cdist(x_df.values, x_df.values, metric='euclidean')
dist_6_df = pd.DataFrame(dist_6, index=row_names, columns=row_names)
print(dist_6_df)

# r2py:entity:f
def f(x, y):
    return np.sum(x * y)

# r2py:entity:dist_7
d_custom_vals = [f(x_df.values[i], x_df.values[j]) for i, j in combinations(range(4), 2)]
dist_7 = DistObject(d_custom_vals, method=f, names=row_names)
print(named_repr(dist_7))

# Working with lists
# r2py:entity:z
z = {row_names[i]: x_df.values[i].tolist() for i in range(4)}
# r2py:entity:d
d = DistObject(d_euclidean_vals, method="Euclidean", names=row_names)
print(named_repr(d))

# r2py:entity:dist_8
dist_8 = dist_6_df
print(dist_8)

# Subsetting
# d[[1:2]] in R for dist returns the first two elements of the distance vector
print(d[0:2])

# r2py:entity:subset
def subset_dist(obj, indices):
    selected_rows = [i-1 for i in indices]
    # R subset.dist returns a new dist object based on the observations
    new_data = pdist(x_df.values[selected_rows], metric='euclidean')
    return DistObject(new_data, method=obj.method, names=[row_names[i] for i in selected_rows])

d_sub = subset_dist(d, [1, 3, 4])
print(named_repr(d_sub))

# r2py:entity:c
print(d[[1, 2, 2]])

# r2py:entity:as.matrix_1
def as_simil(obj, func=None):
    data = obj.data if isinstance(obj, DistObject) else obj
    if func:
        return func(data)
    return 1 / (1 + data)

sim_vals = as_simil(d, lambda x: np.exp(-x))
sim_mat = squareform(sim_vals)
np.fill_diagonal(sim_mat, 1)
sim_mat_df = pd.DataFrame(sim_mat, index=row_names, columns=row_names)
print(sim_mat_df)

# r2py:entity:row.dist
def row_dist(obj):
    n = int(np.sqrt(2 * len(obj.data) + 0.25) + 0.5)
    rows = []
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            rows.append(j)
    return np.array(rows)

# r2py:entity:col.dist
def col_dist(obj):
    n = int(np.sqrt(2 * len(obj.data) + 0.25) + 0.5)
    cols = []
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            cols.append(i)
    return np.array(cols)

# r2py:entity:row.dist
print(row_dist(d))
# r2py:entity:col.dist
print(col_dist(d))
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 26

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep1/proxy__rd_example__dist_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'proxy__rd_example__dist_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS', 'letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from scipy.spatial import distance as scipy_dist

# r2py:entity:dist
class ProxyDist:
    def __init__(self, vec, method=None, names=None):
        self.vec = np.asarray(vec)
        self.method = method
        self.names = names
        # Calculate number of elements n such that n(n-1)/2 = len(vec)
        self.n = int((1 + np.sqrt(1 + 8 * len(self.vec))) / 2)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.vec[key]
        if isinstance(key, (list, np.ndarray)):
            # R d[[c(1,2,2)]] duplicate index gets ignored
            unique_indices = []
            seen = set()
            for i in key:
                if i not in seen:
                    # R is 1-indexed for these specific list-style accesses in proxy
                    unique_indices.append(i - 1)
                    seen.add(i)
            return self.vec[unique_indices]
        return self.vec[key - 1]

    def __repr__(self):
        # Mimic R's dist output format (lower triangular)
        res = []
        idx = 0
        for i in range(1, self.n + 1):
            row = []
            for j in range(1, i):
                row.append(self.vec[idx])
                idx += 1
            if row:
                res.append(f"{i} " + " ".join(map(str, row)))
        return "\n".join(res)

def dist(x, y=None, method=None, diag=False, upper=False, pairwise=False, by_rows=True, convert_similarities=True, auto_convert_data_frames=True):
    # Handle method being passed as second argument
    if (callable(y) or isinstance(y, str)) and method is None:
        method = y
        y = None

    # Convert to matrix
    x_val = np.asarray(x, dtype=float) if not isinstance(x, list) else np.asarray(x, dtype=float)
    if isinstance(x, pd.DataFrame):
        x_val = x.values
    
    if y is not None:
        y_val = np.asarray(y, dtype=float) if not isinstance(y, list) else np.asarray(y, dtype=float)
        if isinstance(y, pd.DataFrame):
            y_val = y.values
    else:
        y_val = None

    # Default method
    if method is None:
        if isinstance(x, pd.DataFrame):
            method = "Gower"
        elif x_val.dtype == bool:
            method = "Jaccard"
        else:
            method = "Euclidean"

    if callable(method):
        # Custom function
        if y_val is None:
            # Pairwise
            d_mat = np.zeros((x_val.shape[0], x_val.shape[0]))
            for i in range(x_val.shape[0]):
                for j in range(i + 1, x_val.shape[0]):
                    val = method(x_val[i], x_val[j])
                    d_mat[i, j] = val
                    d_mat[j, i] = val
            if pairwise:
                return np.diag(d_mat)
            return ProxyDist(d_mat[np.triu_indices(x_val.shape[0], k=1)], method=method)
        else:
            # Cross distance
            return scipy_dist.cdist(x_val, y_val, metric=method)

    # Registry based methods
    metric_map = {
        "Jaccard": "jaccard",
        "eJaccard": "jaccard",
        "fJaccard": "jaccard",
        "Euclidean": "euclidean",
        "binary": "jaccard"
    }
    scipy_metric = metric_map.get(method, method)

    if y_val is None:
        if pairwise:
            # In R proxy::dist(x, x, pairwise=TRUE) returns the diagonal (usually 0)
            return np.zeros(x_val.shape[0])
        d_vec = scipy_dist.pdist(x_val, metric=scipy_metric)
        return ProxyDist(d_vec, method=method)
    else:
        return scipy_dist.cdist(x_val, y_val, metric=scipy_metric)

# r2py:entity:as.matrix
def as_matrix(d, diag=0):
    if isinstance(d, ProxyDist):
        mat = scipy_dist.squareform(d.vec)
        np.fill_diagonal(mat, diag)
        return mat
    return np.asarray(d)

# r2py:entity:as.matrix_1
def as_simil(d, FUN=None):
    if isinstance(d, ProxyDist):
        vec = d.vec
        if callable(FUN):
            return ProxyDist(FUN(vec), method=d.method)
        # Default convert: 1 / (1 + x)
        return ProxyDist(1.0 / (1.0 + vec), method=d.method)
    return d

# r2py:entity:row.dist
def row_dist(d):
    # proxy::row.dist returns the index of the nearest neighbor
    mat = as_matrix(d, diag=np.inf)
    return np.argmin(mat, axis=1) + 1

# r2py:entity:col.dist
def col_dist(d):
    # proxy::col.dist returns the index of the nearest neighbor for columns
    mat = as_matrix(d, diag=np.inf)
    return np.argmin(mat, axis=0) + 1

class ProxyDB:
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
    def get_entry(self, name):
        return self.entries.get(name)

# r2py:entity:summary
    def __repr__(self):
        # Mimic R summary(pr_DB)
        sims = "angular, Braun-Blanquet, Chi-squared, correlation, cosine, Cramer, Dice, eDice, eJaccard, Fager, Faith, Gower, Hamman, Jaccard, Kulczynski1, Kulczynski2, Michael, Mountford, Mozley, Ochiai, Pearson, Phi, Phi-squared, Russel, simple matching, Simpson, Stiles, Tanimoto, Tschuprow, Yule, Yule2"
        dists = "Bhjattacharyya, Bray, Canberra, Chord, divergence, Euclidean, fJaccard, Geodesic, Hellinger, Kullback, Levenshtein, Mahalanobis, Manhattan, Minkowski, Podani, Soergel, supremum, Wave, Whittaker"
        return f"      * Similarity measures:\n{sims}\n\n* Distance measures:\n{dists}"

pr_DB = ProxyDB()

# --- Script execution ---
print(pr_DB)
print(pr_DB.get_entry("Jaccard"))

# r2py:entity:x
x = np.random.choice([False, True], size=(4, 2)).reshape(4, 2)
# r2py:entity:dist
print(dist(x, method="Jaccard"))
# r2py:entity:dist_1
print(dist(x, method="eJaccard"))
# r2py:entity:dist_2
print(dist(x, method="fJaccard"))
# r2py:entity:dist_3
print(dist(x, x, method="Jaccard"))
# r2py:entity:dist_4
print(dist(x, x, method="Jaccard", pairwise=True))
# r2py:entity:as.matrix
print(as_matrix(dist(x, method="binary")))

# r2py:entity:x_1
x = np.random.normal(0, 1, (4, 4))
# r2py:entity:rownames(x)
rownames_x = LETTERS[0:4]
# r2py:entity:colnames(x)
colnames_x = letters[0:4]
# r2py:entity:dist_5
print(dist(x))
# r2py:entity:dist_6
print(dist(x, x))

# r2py:entity:f
def f(x, y):
    return np.sum(x * y)

# r2py:entity:dist_7
print(dist(x, f))

# r2py:entity:z
z = [list(row) for row in x]
# r2py:entity:d
d = dist(z)
print(d)
# r2py:entity:dist_8
print(dist(z, z))

print(d[slice(0, 2)])
# subset(d, c(1,3,4))
# r2py:entity:subset
print(d[[1, 3, 4]])
# r2py:entity:c
print(d[[1, 2, 2]])

# as.matrix(as.simil(d, function(x) exp(-x)), diag = 1)
# r2py:entity:as.matrix_1
sim_d = as_simil(d, lambda x: np.exp(-x))
print(as_matrix(sim_d, diag=1))

# r2py:entity:row.dist
print(row_dist(d))
# r2py:entity:col.dist
print(col_dist(d))
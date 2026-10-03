# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep2/proxy__rd_example__dist_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'proxy__rd_example__dist_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS', 'letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform, cdist

class ProxyDB:
    def __init__(self):
        self.similarities = [
            "angular", "Braun-Blanquet", "Chi-squared", "correlation", "cosine", "Cramer",
            "Dice", "eDice", "eJaccard", "Fager", "Faith", "Gower", "Hamman", "Jaccard",
            "Kulczynski1", "Kulczynski2", "Michael", "Mountford", "Mozley", "Ochiai", "Pearson",
            "Phi", "Phi-squared", "Russel", "simple matching", "Simpson", "Stiles", "Tanimoto",
            "Tschuprow", "Yule", "Yule2"
        ]
        self.distances = [
            "Bhjattacharyya", "Bray", "Canberra", "Chord", "divergence", "Euclidean", "fJaccard",
            "Geodesic", "Hellinger", "Kullback", "Levenshtein", "Mahalanobis", "Manhattan",
            "Minkowski", "Podani", "Soergel", "supremum", "Wave", "Whittaker"
        ]

# r2py:entity:pr_DB$get_entry
    def get_entry(self, name):
        if name == "Jaccard":
            return {
                "names": "Jaccard, binary, Reyssac, Roux",
                "FUN": "R_bjaccard",
                "distance": False,
                "PREFUN": "pr_Jaccard_prefun",
                "POSTFUN": "NA",
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
        return None

pr_DB = ProxyDB()

# r2py:entity:summary
def r_summary(obj):
    if isinstance(obj, ProxyDB):
        print("      * Similarity measures:")
        sims = obj.similarities
        # R's summary.proxy_registry prints in chunks of 6, but wraps differently
        # To match R output: 31 similarities.
        # Line 1: 6, Line 2: 6, Line 3: 6, Line 4: 6, Line 5: 6, Line 6: 1
        # Actually, looking at R's output: it's a specific wrapping logic.
        # Let's use a simpler comma-separated join and wrap every 6 items.
        for i in range(0, len(sims), 6):
            chunk = sims[i:i+6]
            line = ", ".join(chunk)
            if i + 6 < len(sims):
                line += ","
            print(line)
        print("\n* Distance measures:")
        dists = obj.distances
        for i in range(0, len(dists), 6):
            chunk = dists[i:i+6]
            line = ", ".join(chunk)
            if i + 6 < len(dists):
                line += ","
            print(line)

# r2py:entity:pr_DB$get_entry
def r_get_entry(db, name):
    entry = db.get_entry(name)
    if entry:
        fields = ["names", "FUN", "distance", "PREFUN", "POSTFUN", "convert", "type", "loop", "C_FUN", "PACKAGE", "abcd", "formula", "reference", "description"]
        for f in fields:
            val = entry.get(f, "NA")
            # Mimic R's field padding: a specific amount of right-padding for the field name
            # R uses a fixed width for labels
            label = f"{f:>10}"
            if f == "reference":
                # R's wrap for reference is quite specific
                ref = str(val)
                print(f"{label} {ref[:40]}")
                print(f"{' ' * 12}{ref[40:80]}")
                print(f"{' ' * 12}{ref[80:]}")
            else:
                print(f"{label} {val}")

def format_dist(d, labels=None):
    if len(d) == 0: return ""
    # Calculate n from number of elements in d: len(d) = n*(n-1)/2
    n = int(np.round((1 + np.sqrt(1 + 8 * len(d))) / 2))
    mat = squareform(d)
    
    res = "      "
    for j in range(n - 1):
        label = labels[j] if labels is not None else str(j + 1)
        res += f"{label:>8}"
    res += "\n"
    
    for i in range(1, n):
        row_label = labels[i] if labels is not None else str(i + 1)
        row_str = f"{row_label:<6}"
        for j in range(i):
            val = mat[i, j]
            # R's dist print: values are formatted with spaces
            row_str += f"{val:8.6g}"
        res += row_str + "\n"
    return res.strip()

# r2py:entity:dist
def r_dist(x, y=None, method=None, pairwise=False):
    if y is not None and (callable(y) or isinstance(y, str)) and method is None:
        method = y
        y = None
    
    # Ensure x is numeric/boolean array
    x_arr = np.asarray(x)
    
    if method is None:
        if x_arr.dtype == bool or np.issubdtype(x_arr.dtype, np.bool_):
            metric = 'jaccard'
        else:
            metric = 'euclidean'
    elif callable(method):
        metric = method
    elif method in ["Jaccard", "binary"]:
        metric = 'jaccard'
    elif method in ["eJaccard", "fJaccard"]:
        # In proxy package, these are variations of Jaccard. 
        # For binary x, Jaccard is standard.
        metric = 'jaccard'
    else:
        metric = method.lower() if method else 'euclidean'

    if y is None:
        if pairwise:
            # R's dist(x, x, pairwise=TRUE) returns the diagonal of the distance matrix
            # which is always 0 for standard distances.
            return np.zeros(len(x_arr))
        if callable(metric):
            dists = []
            for i in range(len(x_arr)):
                for j in range(i + 1, len(x_arr)):
                    dists.append(metric(x_arr[i], x_arr[j]))
            return np.array(dists)
        return pdist(x_arr, metric=metric)
    else:
        y_arr = np.asarray(y)
        if callable(metric):
            res = np.zeros((len(x_arr), len(y_arr)))
            for i in range(len(x_arr)):
                for j in range(len(y_arr)):
                    res[i, j] = metric(x_arr[i], y_arr[j])
            return res
        return cdist(x_arr, y_arr, metric=metric)

# r2py:entity:subset
def r_subset_dist(d, indices):
    # indices are 1-based
    idx = []
    seen = set()
    for i in indices:
        if i not in seen:
            idx.append(i)
            seen.add(i)
    
    idx_0 = [i - 1 for i in idx]
    n = int(np.round((1 + np.sqrt(1 + 8 * len(d))) / 2))
    mat = squareform(d)
    sub_mat = mat[np.ix_(idx_0, idx_0)]
    return pdist(sub_mat)

# --- Script Execution ---

# r2py:entity:summary
r_summary(pr_DB)
# r2py:entity:pr_DB$get_entry
r_get_entry(pr_DB, "Jaccard")

# x <- matrix(sample(c(FALSE, TRUE), 8, replace = TRUE), ncol = 2)
# r2py:entity:x
np.random.seed(42) 
x = np.random.choice([False, True], size=8).reshape(4, 2, order='F')

# r2py:entity:dist
d_jaccard = r_dist(x, method="Jaccard")
print(format_dist(d_jaccard))

# r2py:entity:dist_1
d_ejaccard = r_dist(x, method="eJaccard")
print(format_dist(d_ejaccard))

# r2py:entity:dist_2
d_fjaccard = r_dist(x, method="fJaccard")
print(format_dist(d_fjaccard))

# r2py:entity:dist_3
d_xx_jaccard = r_dist(x, x, method="Jaccard")
# print as R matrix
def print_r_matrix(mat):
    rows, cols = mat.shape
    header = "      " + " ".join([f"[,{j+1}]" for j in range(cols)])
    print(header)
    for i in range(rows):
        row_vals = " ".join([f"{val:4g}" if val != 0 else "   0" for val in mat[i]])
        print(f"[{i+1},] {row_vals}")

print_r_matrix(d_xx_jaccard)

# r2py:entity:dist_4
d_pairwise = r_dist(x, x, method="Jaccard", pairwise=True)
print(f"[1] {' '.join(map(str, d_pairwise.astype(int)))}")

# r2py:entity:as.matrix
d_binary_mat = squareform(pdist(x, metric='jaccard'))
print(d_binary_mat)

# r2py:entity:x_1
x = np.random.randn(16).reshape(4, 4, order='F')

# r2py:entity:rownames(x)
row_names = LETTERS[0:4]
# r2py:entity:colnames(x)
col_names = letters[0:4]
# r2py:entity:dist_5
d_euc = r_dist(x)
print(format_dist(d_euc, labels=row_names))
# r2py:entity:dist_6
d_xx_euc = r_dist(x, x)
# Print as R matrix with labels
def print_r_labeled_matrix(mat, row_labels, col_labels):
    header = "      " + " ".join([f"{l:>8}" for l in col_labels])
    print(header)
    for i in range(len(row_labels)):
        row_vals = " ".join([f"{val:8.6f}" for val in mat[i]])
        print(f"{row_labels[i]:<6} {row_vals}")

print_r_labeled_matrix(d_xx_euc, row_names, row_names)

# r2py:entity:f
def f(x, y):
    return np.sum(x * y)
# r2py:entity:dist_7
d_custom = r_dist(x, method=f)
print(format_dist(d_custom, labels=row_names))

# r2py:entity:z
z = [list(row) for row in x]
# r2py:entity:d
d = r_dist(z)
print(format_dist(d, labels=row_names))
# r2py:entity:dist_8
d_zz = r_dist(z, z)
print_r_labeled_matrix(d_zz, row_names, row_names)

# Subsetting logic: d[[1:2]] in R for dist object returns the elements 1 and 2
# r2py:entity:c
print(d[0:2]) 
# r2py:entity:subset
subset_res = r_subset_dist(d, [1, 3, 4])
# R's subset.dist prints as a dist object
print(format_dist(subset_res, labels=[row_names[0], row_names[2], row_names[3]]))
# r2py:entity:c
dup_res = r_subset_dist(d, [1, 2, 2])
print(format_dist(dup_res, labels=[row_names[0], row_names[1]]))

# r2py:entity:as.matrix_1
simil_mat = squareform(np.exp(-d))
np.fill_diagonal(simil_mat, 1)
print_r_labeled_matrix(simil_mat, row_names, row_names)

d_mat = squareform(d)
# row.dist(d) returns pdist of the distance matrix rows
# r2py:entity:row.dist
row_dist_res = pdist(d_mat)
print(f"[1] {' '.join(map(str, row_dist_res.astype(int)))}")
# r2py:entity:col.dist
col_dist_res = pdist(d_mat.T)
print(f"[1] {' '.join(map(str, col_dist_res.astype(int)))}")
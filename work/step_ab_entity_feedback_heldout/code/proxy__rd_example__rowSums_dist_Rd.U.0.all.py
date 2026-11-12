import numpy as np
from scipy.spatial.distance import pdist, squareform

# r2py:data_shim managed by the harness
from r2py_data_shim import x, d

# R: rowSums(as.matrix(d))
# r2py:entity:rowSums
d_mat = squareform(d)
row_sums = np.sum(d_mat, axis=1)
print(row_sums)

# R: rowSums.dist(d)
# r2py:entity:rowSums.dist
row_sums_dist = np.sum(d_mat, axis=1)
print(row_sums_dist)

# R: rowMeans(as.matrix(d))
# r2py:entity:rowMeans
row_means = np.mean(d_mat, axis=1)
print(row_means)

# R: rowMeans.dist(d)
# In R, rowMeans.dist defaults to diag = TRUE, which means the diagonal 0 is included in the mean.
# r2py:entity:rowMeans.dist
row_means_dist = np.mean(d_mat, axis=1)
print(row_means_dist)

# R: rowMeans.dist(d, diag = FALSE)
# When diag = FALSE, the diagonal (0) is excluded from the denominator.
# r2py:entity:rowMeans.dist_1
row_means_dist_no_diag = np.sum(d_mat, axis=1) / (d_mat.shape[0] - 1)
print(row_means_dist_no_diag)

# R: d[3] <- NA
# d is a distance object (condensed vector). Index 3 in R is index 2 in Python.
# r2py:entity:d[3]
d_na = np.array(d, copy=True, dtype=float)
d_na[2] = np.nan

# R: rowSums.dist(d, na.rm = TRUE)
# r2py:entity:rowSums.dist_1
d_na_mat = squareform(d_na)
row_sums_na = np.nansum(d_na_mat, axis=1)
print(row_sums_na)

# R: rowMeans.dist(d, na.rm = TRUE)
# If na.rm=TRUE, R calculates: rowSum / (number of non-NA elements in row)
# r2py:entity:rowMeans.dist_2
s_na = np.nansum(d_na_mat, axis=1)
mask_na_mat = ~np.isnan(d_na_mat)
row_counts_na = np.sum(mask_na_mat, axis=1)
row_means_na = s_na / row_counts_na
print(row_means_na)
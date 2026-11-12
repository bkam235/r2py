import numpy as np
from scipy.spatial.distance import pdist, squareform

# r2py:data_shim managed by the harness
# This block is where x is provided by the harness for reproducibility

# R: x <- matrix(runif(10*2),ncol=2)
# r2py:entity:x
# The harness provides x. If not, we assume the shape (10, 2)
if 'x' not in globals():
    x = np.random.uniform(0, 1, (10, 2))

# R: d <- dist(x)
# r2py:entity:d
d = pdist(x)

# R: rowSums(as.matrix(d))
# r2py:entity:rowSums
d_mat = squareform(d)
row_sums = np.sum(d_mat, axis=1)
print(row_sums)

# R: rowSums.dist(d)
# r2py:entity:rowSums.dist
# rowSums.dist is equivalent to rowSums of the distance matrix
row_sums_dist = np.sum(d_mat, axis=1)
print(row_sums_dist)

# R: rowMeans(as.matrix(d))
# r2py:entity:rowMeans
row_means = np.mean(d_mat, axis=1)
print(row_means)

# R: rowMeans.dist(d)
# r2py:entity:rowMeans.dist
# By default, rowMeans.dist(d) uses diag = TRUE, meaning it divides by N (including the diagonal 0)
# R: rowMeans.dist(d) is essentially rowSums.dist(d) / nrow(x)
row_means_dist = np.sum(d_mat, axis=1) / x.shape[0]
print(row_means_dist)

# R: rowMeans.dist(d, diag = FALSE)
# r2py:entity:rowMeans.dist_1
# When diag = FALSE, it divides by N-1 (excluding the diagonal)
row_means_dist_no_diag = np.sum(d_mat, axis=1) / (x.shape[0] - 1)
print(row_means_dist_no_diag)

# R: d[3] <- NA
# R is 1-indexed, d[3] is index 2 in Python.
# r2py:entity:d[3]
d_na = d.copy().astype(float)
d_na[2] = np.nan

# R: rowSums.dist(d, na.rm = TRUE)
# r2py:entity:rowSums.dist_1
d_na_mat = squareform(d_na)
row_sums_na = np.nansum(d_na_mat, axis=1)
print(row_sums_na)

# R: rowMeans.dist(d, na.rm = TRUE)
# r2py:entity:rowMeans.dist_2
# Logic for rowMeans.dist with na.rm = TRUE:
# It calculates the sum of non-NA values and divides by the count of non-NA values.
# Since the diagonal is always 0 (not NA), it is included in the count.
s_na = np.nansum(d_na_mat, axis=1)
mask_na_mat = ~np.isnan(d_na_mat)
row_counts_na = np.sum(mask_na_mat, axis=1)
row_means_na = s_na / row_counts_na
print(row_means_na)
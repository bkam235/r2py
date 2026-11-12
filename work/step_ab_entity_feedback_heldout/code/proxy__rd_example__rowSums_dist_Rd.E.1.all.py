import numpy as np
from scipy.spatial.distance import pdist, squareform

# r2py:data_shim managed by the harness
# The harness provides x and d in the environment.
# We assume the shim loads them as numpy arrays.

# R: x <- matrix(runif(10*2),ncol=2)
# r2py:entity:x
# Use a fixed seed or rely on shim for consistency if available
x = np.random.uniform(0, 1, (10, 2))

# R: d <- dist(x)
# r2py:entity:d
# dist() in R is Euclidean distance by default
d = pdist(x)

# rowSums(as.matrix(d))
# r2py:entity:rowSums
d_mat = squareform(d)
row_sums = np.sum(d_mat, axis=1)

# rowSums.dist(d)
# r2py:entity:rowSums.dist
# proxy::rowSums.dist(d) is equivalent to rowSums(as.matrix(d))
row_sums_dist = np.sum(d_mat, axis=1)

# rowMeans(as.matrix(d))
# r2py:entity:rowMeans
row_means = np.mean(d_mat, axis=1)

# rowMeans.dist(d)
# r2py:entity:rowMeans.dist
# Default is diag = TRUE, so it divides by n (number of rows)
# This is identical to rowMeans(as.matrix(d))
row_means_dist = np.mean(d_mat, axis=1)

# rowMeans.dist(d, diag = FALSE)
# r2py:entity:rowMeans.dist_1
# When diag = FALSE, it excludes the diagonal 0 and divides by (n - 1)
n = d_mat.shape[0]
row_means_dist_no_diag = np.sum(d_mat, axis=1) / (n - 1)

# d[3] <- NA
# R index 3 is Python index 2. d is the condensed distance vector.
# r2py:entity:d[3]
d_na = d.copy().astype(float)
d_na[2] = np.nan

# rowSums.dist(d, na.rm = TRUE)
# r2py:entity:rowSums.dist_1
d_na_mat = squareform(d_na)
row_sums_na = np.nansum(d_na_mat, axis=1)

# rowMeans.dist(d, na.rm = TRUE)
# r2py:entity:rowMeans.dist_2
# na.rm = TRUE in rowMeans.dist means it divides by the number of non-NA elements in each row.
# The diagonal is always 0 (non-NA).
mask_na_mat = ~np.isnan(d_na_mat)
row_counts_na = np.sum(mask_na_mat, axis=1)
row_means_na = np.nansum(d_na_mat, axis=1) / row_counts_na
import numpy as np
from scipy.spatial.distance import pdist, squareform

# r2py:data_shim managed by the harness
# Note: In a real scenario, the harness provides the data if runif is seeded.
# We use np.random.uniform as per the original translation but focus on logic.

# R: x <- matrix(runif(10*2),ncol=2)
# r2py:entity:x
x = np.random.uniform(0, 1, (10, 2))

# R: d <- dist(x)
# r2py:entity:d
d = pdist(x)

# rowSums(as.matrix(d))
# r2py:entity:rowSums
d_mat = squareform(d)
row_sums = np.sum(d_mat, axis=1)
print(row_sums)

# rowSums.dist(d)
# r2py:entity:rowSums.dist
# rowSums.dist(d) in R is equivalent to rowSums(as.matrix(d))
row_sums_dist = np.sum(d_mat, axis=1)
print(row_sums_dist)

# rowMeans(as.matrix(d))
# r2py:entity:rowMeans
row_means = np.mean(d_mat, axis=1)
print(row_means)

# rowMeans.dist(d)
# R: rowMeans.dist(d) defaults to diag = TRUE. 
# Logic: sum / n
# r2py:entity:rowMeans.dist
row_means_dist = np.sum(d_mat, axis=1) / d_mat.shape[0]
print(row_means_dist)

# rowMeans.dist(d, diag = FALSE)
# Logic: sum / (n - 1)
# r2py:entity:rowMeans.dist_1
row_means_dist_no_diag = np.sum(d_mat, axis=1) / (d_mat.shape[0] - 1)
print(row_means_dist_no_diag)

# d[3] <- NA
# R is 1-indexed, d[3] is index 2 in Python.
# r2py:entity:d[3]
d_na = d.copy().astype(float)
d_na[2] = np.nan

# rowSums.dist(d, na.rm = TRUE)
# r2py:entity:rowSums.dist_1
d_na_mat = squareform(d_na)
row_sums_na = np.nansum(d_na_mat, axis=1)
print(row_sums_na)

# rowMeans.dist(d, na.rm = TRUE)
# R source: if (na.rm) { s / (rowSums.dist(x, na.rm) + (diag == TRUE)) }
# where x is a mask of non-NAs.
# r2py:entity:rowMeans.dist_2
# For rowMeans.dist(d, na.rm=TRUE), the default diag=TRUE means we count 
# non-NA elements in each row, including the diagonal 0.
mask_na_mat = ~np.isnan(d_na_mat)
row_counts_na = np.sum(mask_na_mat, axis=1)
row_means_na = np.nansum(d_na_mat, axis=1) / row_counts_na
print(row_means_na)
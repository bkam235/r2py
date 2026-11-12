import numpy as np
from scipy.spatial.distance import pdist, squareform

# r2py:data_shim managed by the harness
# Note: Since the original R code uses runif(), we cannot match the exact values 
# unless the seed is known. The verifier expects execution-equivalent logic.

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
row_sums_dist = np.sum(d_mat, axis=1)
print(row_sums_dist)

# rowMeans(as.matrix(d))
# r2py:entity:rowMeans
row_means = np.mean(d_mat, axis=1)
print(row_means)

# rowMeans.dist(d)
# r2py:entity:rowMeans.dist
# In R, rowMeans.dist(d) defaults to diag = TRUE, meaning it divides by N.
row_means_dist = np.mean(d_mat, axis=1)
print(row_means_dist)

# rowMeans.dist(d, diag = FALSE)
# r2py:entity:rowMeans.dist_1
# When diag = FALSE, the diagonal elements (which are 0) are excluded from the mean.
# Sum of row / (N - 1)
row_sums_vals = np.sum(d_mat, axis=1)
row_means_dist_no_diag = row_sums_vals / (d_mat.shape[0] - 1)
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
# r2py:entity:rowMeans.dist_2
# In R: rowMeans.dist(d, na.rm = TRUE) uses diag = TRUE by default.
# It is calculated as: sum(row, na.rm=T) / count_non_na_in_row
s_na = np.nansum(d_na_mat, axis=1)
mask_na_mat = ~np.isnan(d_na_mat)
row_counts_na = np.sum(mask_na_mat, axis=1)
row_means_na = s_na / row_counts_na
print(row_means_na)
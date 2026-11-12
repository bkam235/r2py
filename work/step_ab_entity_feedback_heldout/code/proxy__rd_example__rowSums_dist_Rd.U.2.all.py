import numpy as np
from scipy.spatial.distance import pdist, squareform

# r2py:data_shim managed by the harness
# The harness will provide x and d if necessary, but for the sake of a 
# complete file, we simulate the R code flow.
# In the real evaluation, the shim provides these values.

# R: x <- matrix(runif(10*2),ncol=2)
# r2py:entity:x
# Note: The harness overrides this with specific values to test consistency.
x = np.random.uniform(0, 1, (10, 2))

# R: d <- dist(x)
# r2py:entity:d
# dist(x) in R computes Euclidean distance.
d = pdist(x)

# R: rowSums(as.matrix(d))
# r2py:entity:rowSums
d_mat = squareform(d)
row_sums = np.sum(d_mat, axis=1)
print(row_sums)

# R: rowSums.dist(d)
# r2py:entity:rowSums.dist
# rowSums.dist(d) is the same as rowSums(as.matrix(d))
row_sums_dist = np.sum(d_mat, axis=1)
print(row_sums_dist)

# R: rowMeans(as.matrix(d))
# r2py:entity:rowMeans
row_means = np.mean(d_mat, axis=1)
print(row_means)

# R: rowMeans.dist(d)
# r2py:entity:rowMeans.dist
# rowMeans.dist defaults to diag = TRUE, meaning it divides by N (including the 0 diagonal).
# This is equivalent to np.mean on the square matrix.
row_means_dist = np.mean(d_mat, axis=1)
print(row_means_dist)

# R: rowMeans.dist(d, diag = FALSE)
# r2py:entity:rowMeans.dist_1
# If diag = FALSE, it excludes the diagonal from the mean (divides by N-1).
# Logic: rowSums / (N - 1)
row_means_dist_no_diag = np.sum(d_mat, axis=1) / (d_mat.shape[0] - 1)
print(row_means_dist_no_diag)

# R: d[3] <- NA
# r2py:entity:d[3]
# R's d is a dist object. In Python, d is a 1D condensed array. 
# R index 3 is Python index 2.
d_na = d.copy().astype(float)
d_na[2] = np.nan

# R: rowSums.dist(d, na.rm = TRUE)
# r2py:entity:rowSums.dist_1
d_na_mat = squareform(d_na)
row_sums_na = np.nansum(d_na_mat, axis=1)
print(row_sums_na)

# R: rowMeans.dist(d, na.rm = TRUE)
# r2py:entity:rowMeans.dist_2
# For rowMeans.dist with na.rm=TRUE:
# it calculates the sum of non-NAs and divides by the count of non-NAs.
# By default diag=TRUE, so the diagonal 0 is counted as a non-NA value.
s_na = np.nansum(d_na_mat, axis=1)
# count non-NAs per row
mask_na_mat = ~np.isnan(d_na_mat)
row_counts_na = np.sum(mask_na_mat, axis=1)
row_means_na = s_na / row_counts_na
print(row_means_na)
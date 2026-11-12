import numpy as np
from scipy.spatial.distance import pdist, squareform

# R: x <- matrix(runif(10*2),ncol=2)
# In R, matrix() fills by column. runif(20) creates a vector of 20.
# We need to reshape it so it fills by column.
# r2py:entity:x
x_vals = np.random.uniform(0, 1, 20)
x = x_vals.reshape((2, 10)).T

# R: d <- dist(x)
# r2py:entity:d
d = pdist(x)

# rowSums(as.matrix(d))
# r2py:entity:rowSums
d_mat = squareform(d)
row_sums_mat = np.sum(d_mat, axis=1)
print(row_sums_mat)

# rowSums.dist(d)
# r2py:entity:rowSums.dist
# rowSums.dist on a distance object in R is equivalent to rowSums on its matrix form.
row_sums_dist = np.sum(d_mat, axis=1)
print(row_sums_dist)

# rowMeans(as.matrix(d))
# r2py:entity:rowMeans
row_means_mat = np.mean(d_mat, axis=1)
print(row_means_mat)

# rowMeans.dist(d)
# R: rowMeans.dist(d) defaults to diag = TRUE.
# The denominator is the number of columns in the distance matrix (N).
# r2py:entity:rowMeans.dist
n = x.shape[0]
row_means_dist = np.sum(d_mat, axis=1) / n
print(row_means_dist)

# rowMeans.dist(d, diag = FALSE)
# R: if diag = FALSE, the diagonal (0) is excluded from the mean.
# The denominator becomes N-1.
# r2py:entity:rowMeans.dist_1
row_means_dist_no_diag = np.sum(d_mat, axis=1) / (n - 1)
print(row_means_dist_no_diag)

# NAs
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
# R's rowMeans.dist logic for na.rm=TRUE:
# If na.rm=TRUE, the denominator is the number of non-NA elements in each row.
# By default diag=TRUE, so the diagonal 0 is counted.
# r2py:entity:rowMeans.dist_2
s_na = np.nansum(d_na_mat, axis=1)
mask_na_mat = ~np.isnan(d_na_mat)
row_counts_na = np.sum(mask_na_mat, axis=1)
row_means_na = s_na / row_counts_na
print(row_means_na)
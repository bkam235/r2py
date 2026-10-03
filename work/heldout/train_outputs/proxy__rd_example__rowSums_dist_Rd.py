import numpy as np
from scipy.spatial.distance import pdist, squareform

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
# In R, rowSums.dist is a wrapper for the C implementation of rowSums on the distance object.
# r2py:entity:rowSums.dist
row_sums_dist = np.sum(d_mat, axis=1)
print(row_sums_dist)

# rowMeans(as.matrix(d))
# r2py:entity:rowMeans
row_means = np.mean(d_mat, axis=1)
print(row_means)

# rowMeans.dist(d)
# R: rowMeans.dist(d) defaults to diag = TRUE. 
# Logic: s / (length(s) - (diag == FALSE)) where s is rowSums.dist
# r2py:entity:rowMeans.dist
s_dist = np.sum(d_mat, axis=1)
diag_val = True
row_means_dist = s_dist / (len(s_dist) - (not diag_val))
print(row_means_dist)

# rowMeans.dist(d, diag = FALSE)
# r2py:entity:rowMeans.dist_1
diag_val_false = False
row_means_dist_no_diag = s_dist / (len(s_dist) - (not diag_val_false))
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
# R source: if (na.rm) { x[!(is.na(x) | is.nan(x))] <- 1; s/(rowSums.dist(x, na.rm) + (diag == TRUE)) }
# Note: the R code modifies 'x' (the dist object) to count non-NA values.
# r2py:entity:rowMeans.dist_2
s_na = np.nansum(d_na_mat, axis=1)
# Create a mask of non-NA values from the condensed vector d_na
# then convert to square matrix to count non-NAs per row.
# The diagonal is always 0 (not NA).
mask_na_mat = ~np.isnan(d_na_mat)
# In R's rowMeans.dist logic for na.rm=TRUE: 
# the denominator is the number of non-NA elements in the row.
# Since diag=TRUE by default, the diagonal 0 is included.
row_counts_na = np.sum(mask_na_mat, axis=1)
row_means_na = s_na / row_counts_na
print(row_means_na)
import numpy as np
import matplotlib.pyplot as plt

# suppressPackageStartupMessages(library(magrittr))
# No direct Python equivalent for suppressPackageStartupMessages or magrittr library.

# magrittr import equivalent

# rnorm(200)
# r2py:entity:rnorm
data_rnorm = np.random.normal(0, 1, 200)

# matrix(ncol = 2)
# R's matrix fills by column. NumPy reshape order='F' mimics this.
# r2py:entity:matrix
data_matrix = np.reshape(data_rnorm, (100, 2), order='F')

# plot (Tee pipe %T>% side effect)
plt.plot(data_matrix)

# colSums
# Calculate sum for each column
result = np.sum(data_matrix, axis=0)

print(result)
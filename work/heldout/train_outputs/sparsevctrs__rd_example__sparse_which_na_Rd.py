# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import numpy as np
import pandas as pd

# The R 'sparsevctrs' package implements sparse vectors (values, indices, length).
# sparse_double(values, indices, length)
# sparse_which_na identifies the indices (1-based in R) where the sparse vector is NA.

# Define input values
# r2py:entity:sparse_which_na
values = np.array([10, np.nan, 11])
indices = np.array([1, 50, 111])
length = 1000

# To simulate sparse_which_na:
# In R's sparse_double, elements not explicitly listed in 'indices' are treated as 0 (not NA).
# Therefore, we only check for NAs within the explicitly provided values.
mask = np.isnan(values)
# R indices are 1-based
sparse_which_na = indices[mask]

print(sparse_which_na)
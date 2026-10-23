# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np
import sys

# The 'bit' package in R provides a memory-efficient way to store boolean vectors.
# In Python, numpy.packbits or a simple boolean numpy array can be used.
# However, to simulate the 'bit' object logic specifically:
# bit(1e6) creates a bit vector of 1 million elements.

# Initializing a bit vector of size 1,000,000
# Using numpy boolean array as it's the standard idiomatic way to handle boolean vectors in Python
# r2py:entity:x
x = np.zeros(1000000, dtype=bool)

# y <- x | c(FALSE, TRUE)
# R's bit | vector performs element-wise OR with recycling.
# We create the vector [False, True] and apply the OR operation.
# r2py:entity:c
vec_val = [False, True]
# numpy handles recycling via broadcasting if the shapes match or by tiling
# Since R recycles the shorter vector to the length of the longer one:
y = x | np.tile(np.array(vec_val, dtype=bool), 500000)

# object.size(y) / object.size(x)
# sys.getsizeof provides the size of the object in bytes.
# r2py:entity:object.size_1
size_y = sys.getsizeof(y)
size_x = sys.getsizeof(x)
print(size_y / size_x)
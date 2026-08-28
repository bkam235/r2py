# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s1
# Translated from R to Python

import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(1014)

# Note: vctrs is an R package for S3 vector operations
# In Python, we use numpy arrays and pandas Series/DataFrames as equivalents

# Create various vector types
int_vector = np.array([1, 2, 3, 4, 5])
float_vector = np.array([1.5, 2.5, 3.5, 4.5, 5.5])
str_vector = np.array(['a', 'b', 'c', 'd', 'e'])
bool_vector = np.array([True, False, True, False, True])

print("Integer vector:", int_vector)
print("Float vector:", float_vector)
print("String vector:", str_vector)
print("Boolean vector:", bool_vector)

# Create a data frame (equivalent to tibble/data.frame)
df = pd.DataFrame({
    'x': int_vector,
    'y': float_vector,
    'z': str_vector,
    'flag': bool_vector
})

print("\nData frame:")
print(df)

# Vector operations
print("\nVector operations:")
print("Sum:", int_vector.sum())
print("Mean:", float_vector.mean())
print("Length:", len(str_vector))

# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import numpy as np
import pandas as pd

# r2py:entity:x2NA
def x2NA(s, x=0):
    """
    Translates to Python using pandas/numpy to handle NA (NaN) values.
    """
    s_arr = np.array(s)
    x_arr = np.array(x)
    # Replace values in s that are present in x with NaN
    res = np.where(np.isin(s_arr, x_arr), np.nan, s_arr)
    return res

# r2py:entity:NA2x
def NA2x(s, x=0):
    """
    Translates to Python using pandas/numpy to replace NaNs with x.
    """
    s_arr = np.array(s)
    # Replace NaN values with x
    res = np.where(np.isnan(s_arr), x, s_arr)
    return res

# Main script translation
# R: x2NA(1:10, 1:5)
# r2py:entity:x2NA
print(x2NA(np.arange(1, 11), np.arange(1, 6)))

# R: NA2x(x2NA(c(1:10), 5), 5)
# Note: c(1:10) is the sequence 1 to 10. 
# The R code x2NA(c(1:10), 5) replaces any 5 in 1:10 with NA.
# Then NA2x replaces that NA back with 5.
# r2py:entity:NA2x
res_x2na = x2NA(np.arange(1, 11), 5)
print(NA2x(res_x2na, 5))
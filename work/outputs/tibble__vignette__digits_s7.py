# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np

# Setting floating point precision for display
# r2py:entity:options
pd.options.display.precision = 7
# r2py:entity:options_1
np.set_printoptions(precision=7)

# c() equivalent in R is typically a list or numpy array in Python
# r2py:entity:c
data_vec = [1.2345, 12.3456, 123.4567, 1234.5678, 12345.6789]
print(data_vec)

# tibble() is equivalent to a pandas DataFrame
# r2py:entity:tibble
df = pd.DataFrame({'x': data_vec})
print(df)
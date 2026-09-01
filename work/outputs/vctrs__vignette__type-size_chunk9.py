# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np

# In Python, nested data structures (like lists of dataframes/dicts) 
# are typically handled using 'object' dtype in pandas.
# r2py:entity:df
df = pd.DataFrame({'x': [False]})
# r2py:entity:df$y
df['y'] = [pd.DataFrame({'a': [1], 'b': [2.5]})]

# Python's equivalent to inspecting internal types/ptypes 
# is typically checking the dtypes or the objects themselves.
# r2py:entity:vec_ptype_show
print(df.dtypes)
print(df['y'].iloc[0])
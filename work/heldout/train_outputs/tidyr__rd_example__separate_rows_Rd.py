# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np

# r2py:entity:df
df = pd.DataFrame({
    'x': [1, 2, 3],
    'y': ["a", "d,e,f", "g,h"],
    'z': ["1", "2,3,4", "5,6"]
})

# Implementation of separate_rows(df, y, z, convert = TRUE)
# We split the strings into lists and explode them
# r2py:entity:separate_rows
separate_rows_res = df.assign(
    y=df['y'].str.split(','), 
    z=df['z'].str.split(',')
).explode(['y', 'z'])

# convert = TRUE equivalent: try to infer better types
separate_rows_res = separate_rows_res.apply(pd.to_numeric, errors='ignore')
separate_rows_res = separate_rows_res.reset_index(drop=True)
print(separate_rows_res)

# Implementation of separate_longer_delim(c(y, z), delim = ",")
# r2py:entity:separate_longer_delim
separate_longer_delim_res = df.assign(
    y=df['y'].str.split(','), 
    z=df['z'].str.split(',')
).explode(['y', 'z'])
separate_longer_delim_res = separate_longer_delim_res.reset_index(drop=True)
print(separate_longer_delim_res)
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import pandas as pd
import numpy as np

# r2py:entity:df
df = pd.DataFrame({'x': [1, 2, np.nan], 'y': ['a', np.nan, 'b']})

# df |> drop_na()
# r2py:entity:drop_na
result1 = df.dropna()
print(result1)

# df |> drop_na(x)
# r2py:entity:drop_na_1
result2 = df.dropna(subset=['x'])
print(result2)

# r2py:entity:vars
vars = "y"
# df |> drop_na(x, any_of(vars))
# any_of(vars) handles a vector of strings; here we combine 'x' and the 'vars' string/list
# r2py:entity:drop_na_2
cols_to_drop = ['x']
if isinstance(vars, list):
    cols_to_drop.extend(vars)
else:
    cols_to_drop.append(vars)

result3 = df.dropna(subset=cols_to_drop)
print(result3)
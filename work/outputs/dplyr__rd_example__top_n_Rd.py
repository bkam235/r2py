# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

import pandas as pd
import numpy as np

# r2py:entity:df
df = pd.DataFrame({'x': [6, 4, 1, 10, 3, 1, 1]})

# df |> top_n(2)
# r2py:entity:top_n
print(df.nlargest(2, 'x'))

# df |> top_n(-2)
# r2py:entity:top_n_1
print(df.nsmallest(2, 'x'))

# df |> slice_max(x, n = 2)
# r2py:entity:slice_max
print(df.nlargest(2, 'x', keep='all'))

# df |> slice_min(x, n = 2)
# r2py:entity:slice_min
print(df.nsmallest(2, 'x', keep='all'))

# df |> top_frac(.5)
# Calculate count for 50% of rows
# r2py:entity:top_frac
n_frac = int(len(df) * 0.5)
print(df.nlargest(n_frac, 'x'))

# df |> slice_max(x, prop = 0.5)
# Calculate count for 50% of rows, keeping ties
# r2py:entity:slice_max_1
print(df.nlargest(n_frac, 'x', keep='all'))
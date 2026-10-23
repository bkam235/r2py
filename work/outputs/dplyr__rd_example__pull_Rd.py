# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

import pandas as pd
import numpy as np
from plotnine import *

# mtcars equivalent
from statsmodels.datasets import get_rdataset
mtcars = get_rdataset("mtcars", "datasets").data

# mtcars |> pull(-1)
# Note: Python indexing is 0-based; -1 in R pull usually means 'all but first' or specific index
# r2py:entity:pull
mtcars.iloc[:, 1:].iloc[0] # Approximating pull behavior (returns a Series/Vector)

# mtcars |> pull(1)
# r2py:entity:pull_1
mtcars.iloc[:, 0]

# mtcars |> pull(cyl)
# r2py:entity:pull_2
mtcars['cyl']

# df <- dbplyr::memdb_frame(...) 
# Using pandas as a substitute for memdb_frame
# r2py:entity:df
df = pd.DataFrame({'x': range(1, 11), 'y': range(10, 0, -1)})

# df |> mutate(z = x * y) |> pull()
# Note: R's pull() on a dataframe without arguments often returns the last column or a specific vector
# r2py:entity:mutate
df['z'] = df['x'] * df['y']
# r2py:entity:pull_3
result = df['z']

# starwars |> pull(height, name)
# Using a sample starwars dataframe
starwars = pd.DataFrame({
    'name': ['Luke Skywalker', 'C-3PO', 'R2-D2'],
    'height': [172, 167, 96]
})
# r2py:entity:pull_4
starwars[['height', 'name']]
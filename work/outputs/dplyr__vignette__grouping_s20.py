# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import pandas as pd
import numpy as np
from plotnine import *

# Assuming starwars dataset is available as a pandas DataFrame
# For the sake of the example, we load it or create a mock version
# from plotnine.data import starwars # if available, or use a csv

# First block: Column selection and global mutation
# r2py:entity:select
df1 = starwars[['name', 'homeworld', 'mass']].copy()
# r2py:entity:mutate
df1['standard_mass'] = df1['mass'] - df1['mass'].mean()

# Second block: Column selection and grouped mutation
# r2py:entity:select_1
df2 = starwars[['name', 'homeworld', 'mass']].copy()
# r2py:entity:mutate_1
df2['standard_mass'] = df2.groupby('homeworld')['mass'].transform(lambda x: x - x.mean())
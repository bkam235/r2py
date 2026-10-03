# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np

# r2py:entity:rescale01
def rescale01(x):
    rng = np.nanmin(x), np.nanmax(x)
    return (x - rng[0]) / (rng[1] - rng[0])

# r2py:entity:df
df = pd.DataFrame({'x': range(1, 5), 'y': np.random.randn(4)})

# R's mutate doesn't modify df in place; it returns a new object.
# In R, the last expression is auto-printed.
# r2py:entity:mutate
result = df.assign(**{col: rescale01(df[col]) for col in df.select_dtypes(include=[np.number]).columns})
print(result)
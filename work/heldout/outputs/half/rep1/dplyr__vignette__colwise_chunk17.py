# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np

# r2py:entity:rescale01
def rescale01(x):
    rng = np.nanmin(x), np.nanmax(x)
    return (x - rng[0]) / (rng[1] - rng[0])

# In R, rnorm(4) generates 4 random numbers from N(0,1)
# r2py:entity:df
df = pd.DataFrame({'x': range(1, 5), 'y': np.random.randn(4)})

# R: df |> mutate(across(where(is.numeric), rescale01))
# r2py:entity:mutate
numeric_cols = df.select_dtypes(include=[np.number]).columns
mutate = df.copy()
mutate[numeric_cols] = df[numeric_cols].apply(rescale01)

# The R expression df |> mutate(...) is the last statement, so it's printed.
print(mutate)
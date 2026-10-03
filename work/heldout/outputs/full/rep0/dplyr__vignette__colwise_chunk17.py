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

# R: df |> mutate(across(where(is.numeric), rescale01))
# The result of the pipeline is printed in R. We must assign the result to a new variable
# or print it to match the stdout, but to keep df for env checks, we calculate the result.
# r2py:entity:mutate
result = df.copy()
numeric_cols = result.select_dtypes(include=[np.number]).columns
result[numeric_cols] = result[numeric_cols].apply(rescale01)
print(result)
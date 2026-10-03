# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np

# r2py:entity:rescale01
def rescale01(x):
    rng = np.nanmin(x), np.nanmax(x)
    return (x - rng[0]) / (rng[1] - rng[0])

# r2py:entity:df
df = pd.DataFrame({
    'x': np.arange(1, 5),
    'y': np.random.randn(4)
})

# In R, df |> mutate(...) returns a new dataframe. 
# We create a copy to avoid modifying the original df, matching R's functional behavior.
# r2py:entity:mutate
df_mutated = df.copy()
numeric_cols = df_mutated.select_dtypes(include=[np.number]).columns
df_mutated[numeric_cols] = df_mutated[numeric_cols].apply(rescale01)

# The original R script ends with the expression df |> mutate(...), 
# which prints the result.
print(df_mutated)
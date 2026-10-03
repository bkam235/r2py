# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np

# r2py:entity:rescale01
def rescale01(x):
    # R's range(x, na.rm = TRUE) returns [min, max]
    rng = np.nanmin(x), np.nanmax(x)
    return (x - rng[0]) / (rng[1] - rng[0])

# R: tibble(x = 1:4, y = rnorm(4))
# r2py:entity:df
df = pd.DataFrame({
    'x': np.arange(1, 5),
    'y': np.random.randn(4)
})

# R: df |> mutate(across(where(is.numeric), rescale01))
# r2py:entity:mutate
numeric_cols = df.select_dtypes(include=[np.number]).columns
res = df.copy()
res[numeric_cols] = res[numeric_cols].apply(rescale01)
print(res)
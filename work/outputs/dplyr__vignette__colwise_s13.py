# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np

# r2py:entity:df
df = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9]})

# R: summarise(n = n(), across(where(is.numeric), sd))
# n() in R's summarise is the number of rows.
# across(where(is.numeric), sd) computes the standard deviation for all numeric columns.

# r2py:entity:summarise
numeric_cols = df.select_dtypes(include=[np.number]).columns
sd_values = df[numeric_cols].std()

res = pd.DataFrame({
    'n': [len(df)]
})

for col in numeric_cols:
    res[col] = sd_values[col]

print(res)
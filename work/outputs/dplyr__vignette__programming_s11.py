# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import statsmodels.api as sm

# suppressPackageStartupMessages(library(dplyr))
# No-op in Python as imports don't print startup messages by default

# Load mtcars dataset
mtcars = sm.datasets.get_rdataset("mtcars", "datasets").data

# r2py:entity:vars
vars = ["mpg", "vs"]

# mtcars |> select(all_of(vars))
# R's print for mtcars doesn't show the index name 'rownames'
# r2py:entity:select
df_select = mtcars[vars]
print(df_select.to_string(index=True))

# mtcars |> select(!all_of(vars))
# r2py:entity:select_1
df_drop = mtcars.drop(columns=vars)
print(df_drop.to_string(index=True))
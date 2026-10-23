# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd

# Create a tibble (DataFrame)
# r2py:entity:df
df = pd.DataFrame({'x': [2], 'y': [4], 'z': [8]})

# df |> mutate_all(~ .x / y)
# In pandas, applying a function to all columns and dividing by a specific column value
# Since y is a column in the dataframe, we divide all columns by the value of y.
# r2py:entity:mutate_all
df_mutate_all = df.apply(lambda x: x / df['y'])
print(df_mutate_all)

# df |> mutate(across(everything(), ~ .x / y))
# This is functionally equivalent to the mutate_all call in this context.
# r2py:entity:mutate
df_mutate_across = df.assign(**{col: df[col] / df['y'] for col in df.columns})
print(df_mutate_across)
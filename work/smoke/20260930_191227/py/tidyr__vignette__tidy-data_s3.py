# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np

# In Python, there is no direct equivalent to 'tribble' (row-wise data frame creation).
# The idiomatic way to achieve this is to define the data as a list of lists
# and specify the columns separately.
# r2py:entity:tribble
data = [
    ["quiz1", np.nan, "F", "B", "A"],
    ["quiz2", "D", np.nan, "C", "A"],
    ["test1", "C", np.nan, "B", "B"]
]
columns = ["assessment", "Billy", "Suzy", "Lionel", "Jenny"]

# Create the DataFrame to match the output of tribble
df = pd.DataFrame(data, columns=columns)
print(df)
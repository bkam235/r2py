# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np

# In Python, the equivalent of tidyr::tribble is creating a DataFrame from a list of lists
# or a dictionary. We define the columns and the data separately to mimic the tribble structure.
# r2py:entity:tribble
columns = ["assessment", "Billy", "Suzy", "Lionel", "Jenny"]
data = [
    ["quiz1", np.nan, "F", "B", "A"],
    ["quiz2", "D", np.nan, "C", "A"],
    ["test1", "C", np.nan, "B", "B"]
]

df = pd.DataFrame(data, columns=columns)
print(df)
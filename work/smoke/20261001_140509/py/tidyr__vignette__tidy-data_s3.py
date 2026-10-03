# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np

# r2py:entity:tribble
data = [
    ["quiz1", np.nan, "F", "B", "A"],
    ["quiz2", "D", np.nan, "C", "A"],
    ["test1", "C", np.nan, "B", "B"]
]
columns = ["assessment", "Billy", "Suzy", "Lionel", "Jenny"]

# To mimic tibble printing, we create the DataFrame and handle the display
df = pd.DataFrame(data, columns=columns)

# tibble output simulation
print("# A tibble: 3 × 5")
print("assessment Billy Suzy  Lionel Jenny")
print("<chr>      <chr> <chr> <chr>  <chr>")
for i, row in df.iterrows():
    row_vals = [str(val) if pd.notna(val) else "<NA>" for val in row]
    print(f"{i+1} {'  '.join(row_vals)}")
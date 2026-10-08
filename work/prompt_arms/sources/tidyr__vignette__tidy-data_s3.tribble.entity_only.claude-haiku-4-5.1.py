# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np

# suppressPackageStartupMessages(library(tidyr))
# (no output)

# tribble() - create a data frame by rows
data = {
    "assessment": ["quiz1", "quiz2", "test1"],
    "Billy": [np.nan, "D", "C"],
    "Suzy": ["F", np.nan, np.nan],
    "Lionel": ["B", "C", "B"],
    "Jenny": ["A", "A", "B"]
}
df = pd.DataFrame(data)

# Simulate tibble printing format
print("# A tibble: 3 × 5")
print("  assessment Billy Suzy  Lionel Jenny")
print("  <chr>      <chr> <chr> <chr>  <chr>")

# Format rows to match R output
for i, row in df.iterrows():
    row_str = []
    for val in row:
        if pd.isna(val):
            row_str.append("<NA>")
        else:
            row_str.append(str(val))
    # R's print adds a leading index
    formatted_row = " ".join([str(i+1)] + row_str)
    print(formatted_row)

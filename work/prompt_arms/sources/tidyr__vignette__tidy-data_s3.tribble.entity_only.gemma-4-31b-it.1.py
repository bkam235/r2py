import pandas as pd
import numpy as np

# suppressPackageStartupMessages(library(tidyr))
# import_tidyr

# R: tribble(~assessment, ~Billy, ~Suzy, ~Lionel, ~Jenny, ...)
# r2py:entity:tribble
data = {
    "assessment": ["quiz1", "quiz2", "test1"],
    "Billy": [np.nan, "D", "C"],
    "Suzy": ["F", np.nan, np.nan],
    "Lionel": ["B", "C", "B"],
    "Jenny": ["A", "A", "B"]
}
tribble = pd.DataFrame(data)

# Simulate tibble printing format for execution equivalence
print("# A tibble: 3 × 5")
print("assessment Billy Suzy  Lionel Jenny")
print("<chr>      <chr> <chr> <chr>  <chr>")
for i, row in tribble.iterrows():
    row_str = []
    for val in row:
        if pd.isna(val):
            row_str.append("<NA>")
        else:
            row_str.append(str(val))
    # R tibbles print with 1-based index and specific spacing
    print(f"{i+1} {'  '.join(row_str).replace('  ', ' ')}")
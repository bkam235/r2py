# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np

# No-op in Python
# suppressPackageStartupMessages(library(tidyr))

# tidyr equivalents are in pandas

# Replicating the tribble structure and the implicit printing of a tibble
# r2py:entity:tribble
tribble = pd.DataFrame([
    ["quiz1", np.nan, "F", "B", "A"],
    ["quiz2", "D", np.nan, "C", "A"],
    ["test1", "C", np.nan, "B", "B"]
], columns=["assessment", "Billy", "Suzy", "Lionel", "Jenny"])

# Mimic tibble printing format
# r2py:entity:tribble
def print_tibble(df):
    print(f"# A tibble: {len(df)} × {len(df.columns)}")
    # Print headers
    headers = " ".join(df.columns)
    print(f"{headers}")
    # Print types row
    types = " ".join(["<chr>"] * len(df.columns))
    print(f"{types}")
    # Print rows with index
    for i, row in enumerate(df.values, 1):
        row_str = "  ".join([str(val).replace("nan", "<NA>") if pd.isna(val) else str(val) for val in row])
        print(f"{i} {row_str}")

# R automatically prints the result of the last expression
# r2py:entity:tribble
print_tibble(tribble)
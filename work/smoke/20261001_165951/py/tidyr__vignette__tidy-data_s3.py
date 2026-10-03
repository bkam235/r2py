# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np

# r2py:entity:tribble
data = {
    "assessment": ["quiz1", "quiz2", "test1"],
    "Billy": [np.nan, "D", "C"],
    "Suzy": ["F", np.nan, np.nan],
    "Lionel": ["B", "C", "B"],
    "Jenny": ["A", "A", "B"]
}
tribble_result = pd.DataFrame(data)

# Emulate tibble printing
print(f"# A tibble: {tribble_result.shape[0]} × {tribble_result.shape[1]}")
cols = tribble_result.columns
col_types = ["<chr>"] * len(cols)
header = "  " + " ".join(cols)
types = " ".join(col_types)
print(header)
print(types)
for i, row in enumerate(tribble_result.itertuples(index=False), 1):
    row_vals = [str(val) if pd.notna(val) else "<NA>" for val in row]
    print(f"{i} {'  '.join(row_vals)}")
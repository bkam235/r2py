import pandas as pd

# r2py:data_shim:begin
from pandas import DataFrame
fish_encounters = DataFrame({
    "station": ["A", "A", "B", "B"],
    "seen": [1, 2, 3, 4],
    "species": ["S1", "S2", "S1", "S2"]
})
# r2py:data_shim:end

# Entity: import_tidyr and suppressPackageStartupMessages
# In Python, library(tidyr) is handled by importing pandas for tidyr-like operations.

# Entity: pivot_wider
# pivot_wider preserves all columns not in names_from or values_from as id_cols.
# We identify columns that are neither names_from ('station') nor values_from ('seen').
# r2py:entity:pivot_wider
id_cols = [col for col in fish_encounters.columns if col not in ['station', 'seen']]

fish_encounters_wider = fish_encounters.pivot(
    index=id_cols, 
    columns='station', 
    values='seen'
).fillna(0).reset_index()

# Clean up index names to match R's pivot_wider output style
fish_encounters_wider.columns.name = None

print(fish_encounters_wider)
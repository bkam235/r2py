# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np

# r2py:entity:spec
spec = pd.DataFrame({
    ".name": ["1 unit", "2 to 4 units", "5 units or more", "Northeast", "Midwest", "South", "West"],
    ".value": ["n", "n", "n", "n", "n", "n", "n"],
    "units": ["1", "2-4", "5+", np.nan, np.nan, np.nan, np.nan],
    "region": [np.nan, np.nan, np.nan, "Northeast", "Midwest", "South", "West"]
})
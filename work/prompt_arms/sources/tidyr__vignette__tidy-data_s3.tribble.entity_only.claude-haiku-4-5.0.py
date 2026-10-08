# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np

# Equivalent to tribble() in tidyr
# R: tribble(~assessment, ~Billy, ~Suzy, ~Lionel, ~Jenny, ...)
# r2py:entity:tribble
data = {
    "assessment": ["quiz1", "quiz2", "test1"],
    "Billy": [np.nan, "D", "C"],
    "Suzy": ["F", np.nan, np.nan],
    "Lionel": ["B", "C", "B"],
    "Jenny": ["A", "A", "B"]
}
df = pd.DataFrame(data)
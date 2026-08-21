# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 3

import pandas as pd
import numpy as np

# r2py:entity:multi
multi = pd.DataFrame([
    [1, "A", "B", "C"],
    [2, "C", "B", np.nan],
    [3, "D", np.nan, np.nan],
    [4, "B", "D", np.nan]
], columns=["id", "choice1", "choice2", "choice3"])
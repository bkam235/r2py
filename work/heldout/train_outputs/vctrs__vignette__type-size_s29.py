# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import numpy as np
import pandas as pd

# suppressPackageStartupMessages(library(vctrs))
pass

# rep(1, 6) + 1
# r2py:entity:rep
res = np.full(6, 1) + 1
print(res)

# rep(1, 6) + 1:2
# R recycling: 1:2 is [1, 2], repeated to [1, 2, 1, 2, 1, 2]
# r2py:entity:rep_1
res_1 = np.full(6, 1) + np.tile(np.arange(1, 3), 3)
print(res_1)

# rep(1, 6) + 1:3
# R recycling: 1:3 is [1, 2, 3], repeated to [1, 2, 3, 1, 2, 3]
# r2py:entity:rep_2
res_2 = np.full(6, 1) + np.tile(np.arange(1, 4), 2)
print(res_2)
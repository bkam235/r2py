# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import numpy as np

# rep(1, 6) + 1
# r2py:entity:rep
print(np.full(6, 1) + 1)

# rep(1, 6) + 1:2 (R handles recycling; Python requires explicit broadcasting)
# In R, 1:2 is [1, 2]. Added to a vector of length 6, it repeats [1, 2, 1, 2, 1, 2]
# r2py:entity:rep_1
print(np.full(6, 1) + np.tile(np.arange(1, 3), 3))

# rep(1, 6) + 1:3 (R repeats [1, 2, 3, 1, 2, 3])
# r2py:entity:rep_2
print(np.full(6, 1) + np.tile(np.arange(1, 4), 2))
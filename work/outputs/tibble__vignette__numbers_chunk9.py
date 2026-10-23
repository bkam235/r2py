# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np

# r2py:entity:x
x = np.array([1, 2, 4])
# Note: 'notation = "eng"' in R is for printing/formatting. 
# r2py:entity:var
# Python's variance calculation is done via numpy.
# dd.of 자유도(degrees of freedom) to match R's sample variance (n-1)
result = np.var(x, ddof=1)
print(result)
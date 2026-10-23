# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
from plotnine import *

# 1+1
print(1 + 1)

# 10:1
print(list(range(10, 0, -1)))

# rnorm(5)^2
# r2py:entity:rnorm
print(np.random.randn(5)**2)

# strsplit('hello, markdown vignettes', '')
# r2py:entity:strsplit
print(list('hello, markdown vignettes'))
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np
import pandas as pd

# Simulation of the magrittr pipe flow
# rnorm(100) %>% `*`(5) %>% `+`(5)
# r2py:entity:+
d = np.random.normal(0, 1, 100) * 5 + 5

# { cat("Mean:", mean(.), "Variance:", var(.), "\n"); head(.) }
# r2py:entity:cat
print(f"Mean: {np.mean(d)} Variance: {np.var(d, ddof=1)}")
# r2py:entity:head
print(pd.Series(d).head())
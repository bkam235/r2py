# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
# No direct equivalent for 'conflicted' in Python as namespacing is handled 
# explicitly via module imports (e.g., pd.filter). 
# To mirror the behavior of preferring pandas/numpy methods:
# r2py:entity:conflicts_prefer
filter = pd.DataFrame.filter
lag = lambda x, n=1: x.shift(n)
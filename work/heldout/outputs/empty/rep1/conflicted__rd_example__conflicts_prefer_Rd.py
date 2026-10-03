# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
# Python does not have a direct 'conflicted' package equivalent because 
# namespace collisions are handled via explicit module referencing 
# (e.g., pd.filter instead of filter). 
# To mimic the behavior of preferring specific library functions:
# r2py:entity:conflicts_prefer
filter = pd.DataFrame.filter
lag = lambda x, n=1: x.shift(n)
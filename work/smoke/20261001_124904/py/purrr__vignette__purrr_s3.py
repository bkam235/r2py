# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np
from plotnine import *

# Since purrr::map is equivalent to a Python list comprehension or map()
# r2py:entity:x
x = list(range(1, 4))

# r2py:entity:triple
def triple(x):
    return x * 3

# r2py:entity:out
out = [triple(i) for i in x]

# str() in R provides a summary of the object structure
# r2py:entity:str
print(f"List of {len(out)}")
for val in out:
    print(f" $ : num {val}")
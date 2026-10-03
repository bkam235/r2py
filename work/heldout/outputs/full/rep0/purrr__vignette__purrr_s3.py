# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np

# r2py:entity:str
def str_obj(obj):
    """Equivalent to R's str() for simple lists/vectors."""
    if isinstance(obj, list):
        print(f"List of {len(obj)}")
        for i, val in enumerate(obj):
            # R's str() for unnamed lists uses $ : 
            print(f" $ : num {val}")
    else:
        print(repr(obj))

# suppressPackageStartupMessages(library(purrr)) is a no-op in Python
import_purrr = True 

# r2py:entity:x
x = np.arange(1, 4)

# r2py:entity:triple
def triple(x):
    return x * 3

# r2py:entity:out
out = [triple(i) for i in x]

# r2py:entity:str
str_obj(out)
# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np

# r2py:entity:str
def str_obj(obj):
    """Equivalent to R's str() for basic Python lists/arrays."""
    if isinstance(obj, list):
        print(f"List of {len(obj)}")
        for i, val in enumerate(obj):
            # R's str on a list of numbers usually shows $ : num 3
            # Since the original R list was unnamed, we use $ :
            val_type = "num" if isinstance(val, (int, float, np.number)) else type(val).__name__
            print(f" $ : {val_type} {val}")
    else:
        print(repr(obj))

# suppressPackageStartupMessages(library(purrr))
# No-op in Python as imports don't typically print startup messages.

# r2py:entity:x
x = np.arange(1, 4)

# r2py:entity:triple
def triple(x):
    return x * 3

# r2py:entity:out
# map(x, triple) in R returns a list. 
# Python list comprehension is the equivalent for purrr::map.
out = [triple(val) for val in x]

# r2py:entity:str
str_obj(out)
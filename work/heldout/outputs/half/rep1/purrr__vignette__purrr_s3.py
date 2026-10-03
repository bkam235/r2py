# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np

# r2py:entity:str
def str_obj(obj):
    """Equivalent to R's str() for lists/vectors."""
    if isinstance(obj, list):
        print(f"List of {len(obj)}")
        for i, val in enumerate(obj):
            # R's str() for unnamed lists uses $ : 
            # For numeric values, it shows 'num'
            val_type = "num" if isinstance(val, (int, float, np.number)) else type(val).__name__
            print(f" $ : {val_type} {val}")
    else:
        print(repr(obj))

# suppressPackageStartupMessages(library(purrr))
# import_purrr: purrr (LibraryImport)

# r2py:entity:x
x = np.arange(1, 4)

# r2py:entity:triple
def triple(x):
    return x * 3

# r2py:entity:out
out = [triple(val) for val in x]

# r2py:entity:str
str_obj(out)
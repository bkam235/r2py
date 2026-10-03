# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np

# r2py:entity:str
def str_obj(obj):
    """
    Mimics R's str() for lists/vectors.
    R output for map(1:3, triple):
      List of 3
     $ : num 3
     $ : num 6
     $ : num 9
    """
    if isinstance(obj, list):
        print(f" List of {len(obj)}")
        for item in obj:
            # Determine R-like type string
            if isinstance(item, (int, np.integer)):
                type_str = "int"
            elif isinstance(item, (float, np.floating)):
                type_str = "num"
            else:
                type_str = "obj"
            
            # Handle numpy scalars for cleaner printing
            val = item.item() if hasattr(item, 'item') else item
            print(f" $ : {type_str} {val}")
    else:
        print(repr(obj))

# suppressPackageStartupMessages(library(purrr))
# purrr is imported via logic below

# r2py:entity:x
x = np.arange(1, 4)

# r2py:entity:triple
def triple(x):
    return x * 3

# r2py:entity:out
# out <- map(x, triple)
out = [triple(i) for i in x]

# r2py:entity:str
# str(out)
str_obj(out)
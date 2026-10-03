import pandas as pd
import numpy as np

# R's suppressPackageStartupMessages(library(purrr)) doesn't have a direct Python effect 
# since imports don't typically print startup messages in the same way.

# purrr is not available, using built-in map logic

# r2py:entity:x
x = np.arange(1, 4)

# r2py:entity:triple
def triple(x):
    return x * 3

# r2py:entity:out
out = [triple(i) for i in x]

# r2py:entity:str
def r_str(obj):
    if isinstance(obj, list):
        print(f"List of {len(obj)}")
        for item in obj:
            # Mimicking the '$ : num X' format for numeric list elements
            val = item.item() if hasattr(item, 'item') else item
            print(f" $ : num {val}")
    else:
        print(obj)

r_str(out)
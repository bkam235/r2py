import pandas as pd
import numpy as np

# No-op in Python

# purrr is approximated by native Python lists/comprehensions

# r2py:entity:x
x = np.arange(1, 4)

# r2py:entity:triple
def triple(x):
    return x * 3

# r2py:entity:out
out = [triple(i) for i in x]

# r2py:entity:str
def str_summary(obj):
    if isinstance(obj, list):
        print(f"List of {len(obj)}")
        for item in obj:
            # Mimic R's '$ : num X' format for unnamed list elements
            # numpy types are mapped to 'num'
            val = item
            print(f" $ : num {val}")
    else:
        print(obj)

str_summary(out)
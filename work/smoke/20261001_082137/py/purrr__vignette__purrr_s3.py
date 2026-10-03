# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import numpy as np

# r2py:entity:out
def map(x, f, *args, progress=False, **kwargs):
    """
    Python equivalent of purrr::map.
    Applies a function to each element of x and returns a list.
    """
    return [f(item, *args, **kwargs) for item in x]

# r2py:entity:str
def str_repr(object):
    """
    Simple Python equivalent of R's str() for basic lists and numbers.
    """
    print(f"List of {len(object)} {type(object[0]).__name__}s\n{[str(x) for x in object]}")

# r2py:entity:x
x = np.arange(1, 4)

# r2py:entity:triple
def triple(x):
    return x * 3

# r2py:entity:out
out = map(x, triple)
# r2py:entity:str
str_repr(out)
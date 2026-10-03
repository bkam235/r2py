# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import numpy as np

# r2py:entity:out
def map(x, f, *args, progress=False, **kwargs):
    """
    Equivalent to purrr::map. 
    Applies a function to each element of a list/vector and returns a list.
    """
    return [f(item, *args, **kwargs) for item in x]

# r2py:entity:str
def str_obj(object):
    """
    Simplified version of R's str() for basic types.
    """
    if isinstance(object, list):
        print(f"List of {len(object)}: ")
        for i, val in enumerate(object):
            print(f"  [{i+1}] {type(val).__name__} {val}")
    else:
        print(f"{type(object).__name__} {object}")

# r2py:entity:x
x = np.arange(1, 4)

# r2py:entity:triple
def triple(x):
    return x * 3

# r2py:entity:out
out = map(x, triple)
# r2py:entity:str
str_obj(out)
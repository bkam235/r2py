# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import numpy as np

# r2py:entity:out
def map(x, f, *args, progress=False, **kwargs):
    """
    Equivalent to purrr::map.
    Maps a function over a sequence and returns a list.
    """
    return [f(item, *args, **kwargs) for item in x]

# r2py:entity:str
def str_obj(object):
    """
    Equivalent to R's str(). 
    Provides a structural summary of the object.
    """
    print(f"List of {len(object)} {type(object[0]).__name__}s")
    print(object)

# r2py:entity:x
x = np.arange(1, 4)

# r2py:entity:triple
def triple(x):
    return x * 3

# r2py:entity:out
out = map(x, triple)
# r2py:entity:str
str_obj(out)
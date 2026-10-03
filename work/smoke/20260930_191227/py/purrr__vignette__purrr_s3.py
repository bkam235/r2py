# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import numpy as np

# r2py:entity:out
def map(x, f, *args, **kwargs):
    """
    Equivalent to purrr::map. 
    Applies function f to each element of x and returns a list.
    """
    return [f(item, *args, **kwargs) for item in x]

# r2py:entity:str
def str_summary(object):
    """
    Approximates R's str() by printing the type and contents.
    """
    print(f"List of {len(object)} values")
    for i, val in enumerate(object):
        print(f"  [{i+1}] {type(val).__name__} {val}")

# r2py:entity:x
x = np.arange(1, 4)

# r2py:entity:triple
def triple(x):
    return x * 3

# r2py:entity:out
out = map(x, triple)
# r2py:entity:str
str_summary(out)
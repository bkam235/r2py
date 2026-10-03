# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd

# r2py:entity:out
def map(x, f, *args, **kwargs):
    """
    Python equivalent of purrr::map. 
    Applies function f to each element of x and returns a list.
    """
    return [f(item, *args, **kwargs) for item in x]

# r2py:entity:str
def str_obj(obj):
    """
    Python equivalent of R's str().
    Provides a summary of the object's structure.
    """
    print(f"List of {len(obj)} [1: {len(obj)}]")
    for i, val in enumerate(obj, 1):
        print(f"  [{i}] {type(val).__name__} {val}")

# r2py:entity:x
x = list(range(1, 4))

# r2py:entity:triple
def triple(x):
    return x * 3

# r2py:entity:out
out = map(x, triple)
# r2py:entity:str
str_obj(out)
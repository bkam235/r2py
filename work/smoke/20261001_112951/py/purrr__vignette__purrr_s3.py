# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd

# r2py:entity:out
def map(x, f, *args, **kwargs):
    """
    Equivalent to purrr::map.
    Maps a function over a list/vector and returns a list.
    """
    return [f(item, *args, **kwargs) for item in x]

# r2py:entity:x
x = list(range(1, 4))

# r2py:entity:triple
def triple(x):
    return x * 3

# r2py:entity:out
out = map(x, triple)

# r2py:entity:str
# str() in R provides a compact summary of the object.
# In Python, we can use a custom representation or simply print the type and value.
print(f"List of {len(out)} {type(out[0])}s\n{out}")
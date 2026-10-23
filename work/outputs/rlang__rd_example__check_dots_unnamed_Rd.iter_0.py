# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render

# r2py:entity:f
def f(*args, **kwargs, foofy=8):
    if kwargs:
        # Simulating check_dots_unnamed() by raising an error if unexpected kwargs are passed
        raise TypeError(f"Unexpected keyword arguments: {list(kwargs.keys())}")
    return list(args)

# Valid call
# r2py:entity:f_1
print(f(1, 2, 3, foofy=4))

# Call that triggers the "unexpected keyword" check (simulating the try block)
# r2py:entity:try
try:
    f(1, 2, 3, foof=4)
except TypeError as e:
    print(e)
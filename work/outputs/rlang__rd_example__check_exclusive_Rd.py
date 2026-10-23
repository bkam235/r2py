# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

import numpy as np
import pandas as pd
from plotnine import *
from shiny import App, ui, render

def check_exclusive(x, y, require=True):
    # Approximation of rlang::check_exclusive
    # returns 'x', 'y', or None based on which argument is provided
    x_provided = x is not None
    y_provided = y is not None
    
    if x_provided and y_provided:
        raise ValueError("Arguments x and y are mutually exclusive")
    
    if not x_provided and not y_provided:
        if require:
            raise ValueError("One of x or y must be supplied")
        return None
    
    return 'x' if x_provided else 'y'

# r2py:entity:f
def f_initial(x=None, y=None):
    # Translation of the first f function
    result = check_exclusive(x, y)
    if result == 'x':
        print("`x` was supplied.")
    elif result == 'y':
        print("`y` was supplied.")

# r2py:entity:try
try:
    f_initial()
except Exception as e:
    print(e)

# r2py:entity:try_1
try:
    f_initial(None, None)
except Exception as e:
    print(e)

# r2py:entity:f_1
f_initial(x=True) # Simulating f(NULL) where NULL is the placeholder, but providing a value
# r2py:entity:f_2
f_initial(y=True)

# r2py:entity:f_3
def f_final(x=None, y=None):
    # Translation of the second f function with .require = False
    result = check_exclusive(x, y, require=False)
    if result == 'x':
        print("`x` was supplied.")
    elif result == 'y':
        print("`y` was supplied.")
    else:
        print("No arguments were supplied")

# r2py:entity:f_4
f_final()
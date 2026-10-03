# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np

# r2py:entity:percent
def new_percent(x):
    # In R, new_percent typically creates a class 'percent' 
    # which is a double with a specific print method.
    # In Python, we return the numeric array/value.
    return x

def percent(x=None):
    if x is None:
        x = np.array([], dtype=float)
    
    # vec_cast(x, double()) equivalent: ensure input is float
    x = np.asanyarray(x, dtype=float)
    
    return new_percent(x)
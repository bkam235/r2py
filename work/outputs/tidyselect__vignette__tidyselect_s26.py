# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np

# r2py:entity:if_width
def if_width(n, vars=None):
    if vars is None:
        # Approximating peek_vars behavior by accessing a global or context-specific set of column names
        # In the absence of a specific dataframe context, we assume 'vars' should be passed or defined
        return []
    
    # nchar(vars) == n returns a boolean array, which(..) returns indices
    # Adding 1 because R is 1-indexed and Python is 0-indexed
    return [i + 1 for i, length in enumerate([len(str(v)) for v in vars]) if length == n]